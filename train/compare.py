# -*- coding:utf-8 -*-
# Author:  zhousf
# Date:    2019-02-15
# Description: 测试两张照片是否同一个人
import config

if __name__ == '__main__':
    first_img = config.TRAIN_MODEL.lfw_dir+'/Aaron_Peirsol/Aaron_Peirsol_0001.png'
    second_img = config.TRAIN_MODEL.lfw_dir+'/Aaron_Eckhart/Aaron_Eckhart_0001.png'
    first_img = '/Users/zhousf/tensorflow/zhousf/data/CASIA-FaceV5/000/000_0.bmp'
    second_img = '/Users/zhousf/tensorflow/zhousf/data/CASIA-FaceV5/001/001_1.bmp'
    config.TRAIN_MODEL.compare(first_img=first_img, second_img=second_img)