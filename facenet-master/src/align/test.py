# -*- coding: utf-8 -*-
import os

command = 'python align_dataset_mtcnn.py --help'

# MTCNN进行人脸检测并裁剪
command = 'python align_dataset_mtcnn.py ' \
          'data/lfw/raw data/lfw/lfw_160 ' \
          '--image_size 160 ' \
          '--margin 32 ' \
          '--random_order'
# 评估
command = 'Python ../validate_on_lfw.py data/lfw/lfw_160 ' \
          '../models/20180402-114759 ' \
          '--lfw_pairs ../../data/pairs.txt'
# 测试 0.6以下为同一个人
command = 'python ../compare.py ' \
          '../models/20180402-114759 ' \
          'data/lfw/lfw_160/Aaron_Peirsol/Aaron_Peirsol_0001.png  ' \
          'data/lfw/lfw_160/Aaron_Peirsol/Aaron_Peirsol_0002.png'
command = 'python ../compare.py ' \
          '../models/20180402-114759 ' \
          'data/lfw/lfw_160/Aaron_Peirsol/Aaron_Peirsol_0001.png  ' \
          'data/lfw/lfw_160/Aaron_Eckhart/Aaron_Eckhart_0001.png'
command = 'python ../compare.py ' \
          '../models/20180402-114759 ' \
          'data/lfw/raw/Aaron_Peirsol/Aaron_Peirsol_0001.jpg  ' \
          'data/lfw/raw/Aaron_Eckhart/Aaron_Eckhart_0001.jpg'
# command = 'python ../compare.py ' \
#           '../models/20180402-114759 ' \
#           'data/lfw/raw/Aaron_Sorkin/Aaron_Sorkin_0001.jpg  ' \
#           'data/lfw/raw/Aaron_Sorkin/Aaron_Sorkin_0002.jpg'
os.system(command)