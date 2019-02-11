# -*- coding:utf-8 -*-
# Author:  zhousf
# Date:    2019-01-25
# Description: 脸部特征提取、存储、查询
# 参考facenet/src/contribute/export_embeddings.py -> load_and_align_data()
import tensorflow as tf
from align import detect_face
import facenet
import numpy as np
import os
from scipy import misc
from annoy import AnnoyIndex
import config
from app import db, User


class FaceEmbeddings(object):
    def __init__(self, face_crop_size=160, face_crop_margin=32):
        self.minsize = 20
        self.threshold = [0.6, 0.7, 0.7]
        self.factor = 0.709
        self.image_size = face_crop_size
        self.margin = face_crop_margin
        with tf.Graph().as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.3)
            sess = tf.Session(
                config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            with sess.as_default():
                self.pnet, self.rnet, self.onet = detect_face.create_mtcnn(sess, None)

    def load_and_align_data(self, image_file):
        """
        :param image_file:
        :return:
        """
        image = misc.imread(os.path.expanduser(image_file))
        bounding_boxes, points = detect_face.detect_face(image, self.minsize, self.pnet, self.rnet,
                                                         self.onet,
                                                         self.threshold, self.factor)
        print(points)
        if len(bounding_boxes) == 0:
            return None
        img_size = np.asarray(image.shape)[0:2]
        det = np.squeeze(bounding_boxes[0, 0:4])
        bb = np.zeros(4, dtype=np.int32)
        bb[0] = np.maximum(det[0] - self.margin / 2, 0)
        bb[1] = np.maximum(det[1] - self.margin / 2, 0)
        bb[2] = np.minimum(det[2] + self.margin / 2, img_size[1])
        bb[3] = np.minimum(det[3] + self.margin / 2, img_size[0])
        cropped = image[bb[1]:bb[3], bb[0]:bb[2], :]
        resize_image = misc.imresize(cropped, (self.image_size, self.image_size), interp='bilinear')
        misc.imsave('im.jpg', resize_image)
        return resize_image


class Annoy(object):
    def __init__(self):
        self.annoy = AnnoyIndex(512)
        self.annoy_index_file = 'face_id'
        self.update_index()

    def update_index(self):
        self.annoy.unload()
        users = User.query.all()
        for user in users:
            self.annoy.add_item(user.id, self.str_to_vector(user.faceId))
        self.annoy.build(100)
        self.annoy.save(self.annoy_index_file)
        self.annoy.load(self.annoy_index_file)

    @staticmethod
    def vector_to_str(vector):
        new_vector = [str(x) for x in vector]
        return ','.join(new_vector)

    @staticmethod
    def str_to_vector(face_str):
        str_list = face_str.split(',')
        return [float(x) for x in str_list]

    def query_face_id(self, face_id):
        return self.annoy.get_nns_by_vector(face_id, 5, include_distances=True)


class FaceFeatureExtractor(object):
    def __init__(self):
        self.model_path = config.CONFIG_SERVER.face_model_file
        self.per_process_gpu_memory_fraction = config.CONFIG_SERVER.per_process_gpu_memory_fraction
        self.face_embeddings = FaceEmbeddings()
        self.annoy = Annoy()
        self.graph = tf.Graph()
        with open(self.model_path) as fd:
            graph_def = tf.GraphDef.FromString(fd.read())
        with self.graph.as_default():
            tf.import_graph_def(graph_def=graph_def, name='')
        tf_config = tf.ConfigProto()
        tf_config.gpu_options.per_process_gpu_memory_fraction = self.per_process_gpu_memory_fraction
        tf_config.gpu_options.allow_growth = True
        self.sess = tf.Session(graph=self.graph, config=tf_config)

    def extract_face_feature(self, image):
        """
        提取脸部特征
        :param image:
        :return: 返回512维度特征向量
        """
        images_placeholder = self.graph.get_tensor_by_name("input:0")
        embeddings = self.graph.get_tensor_by_name("embeddings:0")
        phase_train_placeholder = self.graph.get_tensor_by_name("phase_train:0")
        face_aligned = self.face_embeddings.load_and_align_data(image)
        if face_aligned is None:
            return None
        face_prewhiten = facenet.prewhiten(face_aligned)
        feed_dict = {images_placeholder: [face_prewhiten], phase_train_placeholder: False}
        return self.sess.run(embeddings, feed_dict=feed_dict)[0]

    def register_face(self, user, image_file):
        if User.query.filter_by(name=user.name).first() is not None:
            return 2, False
        face_id = self.extract_face_feature(image_file)
        if face_id is None:
            return 1, False
        user.faceId = self.annoy.vector_to_str(face_id)
        db.session.add(user)
        db.session.commit()
        if user.id is not None:
            self.annoy.update_index()
            return 0, True
        else:
            return 2, False

    def query_face(self, image_file):
        face_id = self.extract_face_feature(image_file)
        if face_id is None:
            return 1, False, None
        faces = self.annoy.query_face_id(face_id)
        print(faces)
        if faces:
            print(str(faces[0][0]) + ' ' + str(faces[1][0]))
            if faces[1][0] < 0.8:
                user = User.query.filter_by(id=faces[0][0]).first()
                if user:
                    return 0, True, user
        return 2, False, None
