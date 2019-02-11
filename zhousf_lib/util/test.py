# -*- coding:utf-8 -*-
# Author:  zhousf
# Date:    2019-01-28
# Description:

import os
from zhousf_lib.util import string_util

path = '/Volumes/zhousf/sy'

for root,dirs,files in os.walk(path):
    for f in files:
        if string_util.not_contain(f,'.'):
            print(f)
            n = os.path.join(root,f)+'.txt'
            os.renames(os.path.join(root,f),n)