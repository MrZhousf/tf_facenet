# -*- coding:utf-8 -*-
# Author:  zhousf
# Date:    2019-02-15
# Description: MTCNN 人脸检测、对齐、裁剪
import config

if __name__ == '__main__':
    input_dir = '/Users/zhousf/tensorflow/zhousf/data/CASIA-FaceV5'
    output_dir = '/Users/zhousf/tensorflow/zhousf/data/CASIA-FaceV5_160'
    config.TRAIN_MODEL.align_dataset_mtcnn(input_dir=input_dir, output_dir=output_dir)
