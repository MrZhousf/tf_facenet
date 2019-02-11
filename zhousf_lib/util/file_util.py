# -*- coding: utf-8 -*-
import os, shutil
import hashlib
import json


# 移动文件到指定目录下
def move_file(srcfile, dst_path):
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    if os.path.exists(srcfile):
        shutil.move(srcfile, dst_path)


# 复制文件到制定的目录下
def copy_file(srcfile, dst_path):
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    if os.path.exists(srcfile):
        shutil.copy(srcfile, dst_path)


# 将目录下所有文件复制到指定目录下：不遍历
def copy_files(src_dir, dst_dir):
    if os.path.exists(dst_dir):
        fl = os.listdir(src_dir)
        for i in range(0, len(fl)):
            print(fl[i])
            copy_file(os.path.join(src_dir, fl[i]), dst_dir)


# 将目录下所有文件覆盖到指定的目录下：遍历
def copy_files_overwrite(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    total = 0
    for root, dirs, files in os.walk(src_dir):
        for cf in files:
            f = os.path.join(root,cf)
            if os.path.exists(f):
                print(f)
                total += 1
                shutil.copy(f, dst_dir)
    print('total='+str(total))




# 将目录下所有jpg文件复制到指定目录下：遍历
def copy_jpg_files(src_dir, dst_dir):
    num = 0
    for root, dirs, files in os.walk(src_dir):
        for file_name in files:
            if file_name.endswith('.jpg') or file_name.endswith('.JPG'):
                if not os.path.exists(dst_dir + '/' + file_name):
                    num += 1
                    print(os.path.join(root, file_name))
                    copy_file(os.path.join(root, file_name), dst_dir)
    print("共：" + str(num))


# 采用md5比较两个文件是否相同
def compare_file(file_a, file_b):
    md5file_a = open(file_a, 'rb')
    md5_a = hashlib.md5(md5file_a.read()).hexdigest()
    md5file_a.close()
    md5file_b = open(file_b, 'rb')
    md5_b = hashlib.md5(md5file_b.read()).hexdigest()
    md5file_a.close()
    print(md5_b)
    return md5_a == md5_b


def md5(file_path):
    md5file = open(file_path, 'rb')
    md5 = hashlib.md5(md5file.read()).hexdigest()
    md5file.close()
    return md5


'''
将目录下的jpg文件以md5重新命名
src_dir：待处理目录
dest_dir：处理后目录
repeat_dir：md5重复文件目录
abort_dir：非jpg文件的杂项目录
'''


def rename_file_with_md5(src_dir, dest_dir, repeat_dir, abort_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    if not os.path.exists(repeat_dir):
        os.makedirs(repeat_dir)
    if not os.path.exists(abort_dir):
        os.makedirs(abort_dir)
    total_num = 0
    repeat_num = 0
    abort_num = 0
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            total_num += 1
            file_path = root + '/' + f
            if not f.endswith('.jpg') and not f.endswith('.JPG'):
                copy_file(file_path, abort_dir)
                abort_num += 1
                continue
            name_new = dest_dir + '/' + md5(file_path) + '.jpg'
            if not os.path.exists(name_new):
                print(name_new)
                os.rename(file_path, name_new)
            else:
                copy_file(file_path, repeat_dir)
                repeat_num += 1
    print('共：' + str(total_num) + '项，有效项：' + str(total_num - repeat_num - abort_num) +
          '，重复项' + str(repeat_num) + '，杂项：' + str(abort_num))


'''
通过xml文件找jpg文件
xml_dir：xml目录
jpg_dir：jpg目录
dst_dir：将匹配的xml与jpg复制的该文件夹下
xml_no_match_dir：未匹配到jpg的xml文件
'''


def find_jpg_by_xml(xml_dir, jpg_dir, dst_dir, xml_no_match_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    if xml_no_match_dir is not None and not os.path.exists(xml_no_match_dir):
        os.makedirs(xml_no_match_dir)
    file_map = {}
    total_num = 0
    xml_num = 0
    for root, dirs, files in os.walk(jpg_dir):
        for file_jpg in files:
            filename = ''
            if file_jpg.endswith('.jpg'):
                filename, ext = file_jpg.split('.jpg')
            if file_jpg.endswith('.JPG'):
                filename, ext = file_jpg.split('.JPG')
            filename = filename + '.xml'
            file_map[filename] = os.path.join(root, file_jpg)
    for root, dirs, files in os.walk(xml_dir):
        for f in files:
            total_num += 1
            file_path = os.path.join(root, f)
            print(file_path)
            if f.endswith('xml') and file_map.has_key(f):
                jpg_file_path = file_map[f]
                copy_file(jpg_file_path, dst_dir)
                copy_file(file_path, dst_dir)
                xml_num += 1
            else:
                if xml_no_match_dir is not None:
                    copy_file(file_path, xml_no_match_dir)
    print('共：' + str(total_num) + ',匹配到：' + str(xml_num))


def find_jpg_by_json(json_dir, jpg_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    file_map = {}
    total_num = 0
    xml_num = 0
    for root, dirs, files in os.walk(jpg_dir):
        for file_jpg in files:
            filename = ''
            if file_jpg.endswith('.jpg'):
                filename, ext = file_jpg.split('.jpg')
            if file_jpg.endswith('.JPG'):
                filename, ext = file_jpg.split('.JPG')
            filename = filename + '.json'
            file_map[filename] = os.path.join(root, file_jpg)
    for root, dirs, files in os.walk(json_dir):
        for f in files:
            total_num += 1
            file_path = os.path.join(root, f)
            print(file_path)
            if f.endswith('json') and file_map.has_key(f):
                jpg_file_path = file_map[f]
                copy_file(jpg_file_path, dst_dir)
                try:
                    copy_file(file_path, dst_dir)
                except Exception:
                    pass
                xml_num += 1
    print('共：' + str(total_num) + ',匹配到：' + str(xml_num))


'''
通过jpg文件找xml文件
xml_dir：xml目录
jpg_dir：jpg目录
dst_dir：将匹配的xml与jpg复制的该文件夹下
xml_no_match_dir：未匹配到xml的jpg文件
'''


def find_xml_by_jpg(xml_dir, jpg_dir, dst_dir, jpg_no_match_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    if not os.path.exists(jpg_no_match_dir):
        os.makedirs(jpg_no_match_dir)
    file_map = {}
    total_num = 0
    jpg_num = 0
    xml_num = 0
    for root, dirs, files in os.walk(jpg_dir):
        for f in files:
            total_num += 1
            if f.endswith('jpg') or f.endswith('.JPG'):
                file_map[f] = os.path.join(root, f)
    for root, dirs, files in os.walk(xml_dir):
        for file_xml in files:
            if file_xml.endswith('.xml'):
                xml_num += 1
                xml_name, ext = file_xml.split('.xml')
                xml_path = os.path.join(root, file_xml)
                if file_map.has_key(xml_name + '.jpg'):
                    print(file_xml)
                    jpg_num += 1
                    copy_file(file_map[xml_name + '.jpg'], dst_dir)
                    copy_file(xml_path, dst_dir)
                if file_map.has_key(xml_name + '.JPG'):
                    print(file_xml)
                    jpg_num += 1
                    copy_file(file_map[xml_name + '.JPG'], dst_dir)
                    copy_file(xml_path, dst_dir)
    print(xml_num)
    print('共：' + str(total_num) + ',匹配到：' + str(jpg_num))


'''
通过jpg文件找xml文件
xml_dir：xml目录
jpg_dir：jpg目录，将找到的xml复制到对应jpg文件目录下
'''


def find_xml_by_jpg_copy(xml_dir, jpg_dir):
    file_map = {}
    total_num = 0
    jpg_num = 0
    xml_num = 0
    for root, dirs, files in os.walk(jpg_dir):
        for f in files:
            total_num += 1
            if f.endswith('jpg') or f.endswith('.JPG'):
                file_map[f] = os.path.join(root, f)
                jpg_num += 1
    for root, dirs, files in os.walk(xml_dir):
        for file_xml in files:
            if file_xml.endswith('.xml'):
                xml_name, ext = file_xml.split('.xml')
                xml_path = os.path.join(root, file_xml)
                if file_map.has_key(xml_name + '.jpg'):
                    xml_num += 1
                    jpg_path = os.path.dirname(file_map[xml_name + '.jpg'])
                    print(jpg_path)
                    copy_file(xml_path, jpg_path)
                if file_map.has_key(xml_name + '.JPG'):
                    xml_num += 1
                    jpg_path = os.path.dirname(file_map[xml_name + '.JPG'])
                    print(jpg_path)
                    copy_file(xml_path, jpg_path)
    print('共：' + str(total_num) + ',jpg=' + str(jpg_num) + ',xml=' + str(xml_num))


'''
通过扩展名删除文件
extension：扩展名例如'.xml'
'''


def delete_file_by_extension(src_dir, extension):
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f.endswith(extension):
                print(root, f)
                os.remove(os.path.join(root, f))


'''
通过文件名删除文件
file_name：'123.xml'
'''


def delete_file_by_name(src_dir, file_name):
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f != file_name:
                continue
            if not os.path.exists(os.path.join(root, f)):
                continue
            print(root, f)
            os.remove(os.path.join(root, f))


# 从dst_dir中删除包含src_dir所有文件
def delete_file_contained(src_dir, dst_dir):
    file_list = []
    ll = os.listdir(src_dir)
    for i in range(0, len(ll)):
        na = ll[i]
        file_list.append(na)
    num = 0
    for root, dirs, files in os.walk(dst_dir):
        for f in files:
            if f in file_list:
                num += 1
                print(os.path.join(root, f))
                os.remove(os.path.join(root, f))
    print(str(num))


'''
将指定目录均分，保持目录结构
data_dir 解释：
例如 /media/ubuntu/zsf/data
会在 /media/ubuntu/zsf/ 目录下新建
data0 ... data3(task_num=3) 
extention：标注文件的扩展名 '.json'
'''


def assign_task(data_dir, task_num, extention):
    dir_name = os.path.basename(data_dir)
    for root, dirs, files in os.walk(data_dir):
        for dir in dirs:
            # 创建目录结构
            for i in range(0, task_num):
                new_dir = os.path.join(root, dir).replace(dir_name, dir_name + '-' + str(i))
                if not os.path.exists(new_dir):
                    os.makedirs(new_dir)
            dir = os.path.join(root, dir)
            lis = os.listdir(dir)
            for i in range(0, len(lis)):
                f = lis[i]
                if extention is not None:
                    if f.endswith(extention):
                        my_path = os.path.join(root, dir, f)
                        w = i % task_num
                        new_path = my_path.replace(dir_name, dir_name + '-' + str(w))
                        jpg, ext = my_path.split(extention)
                        print(os.path.dirname(new_path))
                        copy_file(my_path, os.path.dirname(new_path))
                        copy_file(jpg + '.jpg', os.path.dirname(new_path))
                        copy_file(jpg + '.JPG', os.path.dirname(new_path))
                else:
                    my_path = os.path.join(root, dir, f)
                    w = i % task_num
                    new_path = my_path.replace(dir_name, dir_name + '-' + str(w))
                    print(new_path)
                    copy_file(my_path, os.path.dirname(new_path))


'''
获取文件扩展名
'''


def file_extension(path):
    return os.path.splitext(path)[1]


'''
获取文件名，不包括路径和扩展名
'''


def file_basename(path):
    fname = os.path.basename(path)
    filename, ext = fname.split('.')
    return filename


'''
获取文件路径，不包括文件名
'''


def file_path(path):
    return os.path.dirname(path)


if __name__ == '__main__':
    # rootdir = '/media/ubuntu/b8f80802-d95a-41c3-b157-6f4e34967425/z-damage-data/data-jingyou/'
    # xml_dir = rootdir+'aoxian'
    # jpg_dir = rootdir + 'aoxian_labelme'
    # # jpg_dir = '/media/ubuntu/b8f80802-d95a-41c3-b157-6f4e34967425/output_whole_20180515'
    # dst_dir = rootdir + 'aoxian1'
    # jpg_no_match_dir = rootdir + 'damage_no_match'
    # find_xml_by_jpg(xml_dir, jpg_dir,dst_dir,jpg_no_match_dir)

    # src_dir=rootdir+'whole-image-100G/dbic0703'
    # dest_dir=rootdir+'whole-image-100G/dbic0703-rename'
    # repeat_dir=rootdir+'whole-image-100G/dbic0703-repeat'
    # abort_dir=rootdir+'whole-image-100G/dbic0703-abort'
    # rename_file_with_md5(src_dir,dest_dir,repeat_dir,abort_dir)

    # rootdir = '/media/ubuntu/b8f80802-d95a-41c3-b157-6f4e34967425/data-banghao/'
    # xml_dir=rootdir+'2019-1-17-xml'
    # jpg_dir='/media/ubuntu/b8f80802-d95a-41c3-b157-6f4e34967425/output_20180117'
    # dst_dir=rootdir+'2019-1-17-whole'
    # xml_no_match_dir=rootdir+'no-match'
    # find_jpg_by_xml(xml_dir,jpg_dir,dst_dir,xml_no_match_dir)

    # rootdir = '/media/ubuntu/b8f80802-d95a-41c3-b157-6f4e34967425/data-banghao/xml-2018-7-12-segment_box/'
    # src_dir = rootdir + 'new-boli'
    # dst_dir = rootdir + 'boli'
    # # copy_files(src_dir,dst_dir)
    # copy_files_overwrite(src_dir,dst_dir)

    # jpg_dir='/media/ubuntu/zhousf/nzm/banghao'
    # xml_dir='/media/ubuntu/b8f80802-d95a-41c3-b157-6f4e34967425/data-banghao/img_20180516/banghao-xml-jpg'
    # find_xml_by_jpg_copy(xml_dir,jpg_dir)

    # json_dir = '/media/ubuntu/zhousf/sy/student'
    # jpg_dir = '/media/ubuntu/b8f80802-d95a-41c3-b157-6f4e34967425/data-banghao/img_20180516/student-xml-jpg'
    # dst_dir = json_dir
    # find_jpg_by_json(json_dir, jpg_dir, dst_dir)

    src_dir = '/media/ubuntu/b8f80802-d95a-41c3-b157-6f4e34967425/data-banghao/2019-1-17-whole'
    assign_task(src_dir, task_num=40, extention='.json')

    # delete_file_by_extension('/media/ubuntu/zhousf/sy/student','.xml')
    # delete_file_by_extension('/media/ubuntu/zhousf/sy/banghao','.xml')
    # delete_file_by_extension('/media/ubuntu/b8f80802-d95a-41c3-b157-6f4e34967425/aaaaa/banghao-seg-jpg-0-delete','.json')
    # delete_file_by_extension('/media/ubuntu/zhousf/nzm/banghao','.xml')
    # delete_file_by_name('/home/ubuntu/zsf/dl/dataset-banghao','img.png')
