# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, abort
import os
import sys
from info import response_info as res
from zhousf_lib.util import string_util, file_util
import base64
import face_feature
import time
from app import User

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

userModel = Blueprint('userModel', __name__, template_folder='../templates')
extractor = face_feature.FaceFeatureExtractor()


@userModel.route("/test", methods=['get'])
def test():
    face_img = ''
    name = ''
    sex = ''
    department = '技术部'
    user = User(name=name, sex=sex, department=department)
    code, success = extractor.register_face(user, face_img)
    if success:
        return res.business('000', '注册成功！')
    else:
        if code == 1:
            return res.business('002', '未检测到人脸，请正视摄像头！')
        else:
            return res.business('003', '用户已存在：' + name)


@userModel.route("/sign_up", methods=['get'])
def sign_up():
    return render_template('sign_up.html', navigation='sign_up')


@userModel.route("/do_sign_up", methods=['post'])
def do_sign_up():
    params = request.form
    if 'name' not in params \
            or 'sex' not in params \
            or 'image' not in params \
            or 'department' not in params:
        return res.business('001', '参数不合法')
    name = params['name']
    if string_util.is_empty(name):
        return res.business('001', '用户名不能为空')
    sex = params['sex']
    if string_util.is_empty(sex):
        return res.business('001', '性别不能为空')
    department = params['department']
    if string_util.is_empty(department):
        return res.business('001', '部门不能为空')
    image = params['image']
    if string_util.is_empty(image):
        return res.business('001', '图片不能为空')
    face_img = os.path.join(file_util.file_path(__file__), '../face_sign_up.jpg')
    if os.path.exists(face_img):
        os.remove(face_img)
    img_data = base64.b64decode(image)
    if img_data is None:
        return res.business('001', '保存图片失败')
    with open(face_img, 'wb') as f:
        f.write(img_data)
    if not os.path.exists(face_img):
        return res.business('001', '保存图片失败')
    user = User(name=name, sex=sex, department=department)
    code, success = extractor.register_face(user, face_img)
    if success:
        return res.business('000', '注册成功！')
    else:
        if code == 1:
            return res.business('002', '未检测到人脸，请正视摄像头！')
        else:
            return res.business('003', '用户已存在：'+name)


@userModel.route("/sign_in", methods=['get'])
def to_sign_in():
    return render_template('sign_in.html', navigation='sign_in')


@userModel.route("/do_sign_in", methods=['post'])
def do_sign_in():
    params = request.form
    if 'image' not in params:
        return res.business('001', '参数不合法')
    image = params['image']
    if string_util.is_empty(image):
        return res.business('001', '图片不能为空')
    face_img = os.path.join(file_util.file_path(__file__), '../face_sign_in.jpg')
    if os.path.exists(face_img):
        os.remove(face_img)
    img_data = base64.b64decode(image)
    if img_data is None:
        return res.business('001', '保存图片失败')
    with open(face_img, 'wb') as f:
        f.write(img_data)
    if not os.path.exists(face_img):
        return res.business('001', '保存图片失败')
    start = time.time()
    code, success, user = extractor.query_face(face_img)
    end = time.time()
    cost = (end - start) * 1000
    print('cost time: ' + str(cost) + ' ms')
    if success:
        sign_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        info = {'name': user.name, 'sex': user.sex, 'department': user.department, 'sign_time': sign_time}
        return res.business('000', '签到成功！', info)
    else:
        if code == 1:
            return res.business('002', '未检测到人脸，请正视摄像头！')
        else:
            return res.business('003', 'Wow...这是谁啊，要和我们一起玩吗？')