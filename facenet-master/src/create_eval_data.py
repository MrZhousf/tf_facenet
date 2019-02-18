# -*- coding:utf-8 -*-
# Author:  zhousf
# Date:    2019-02-18
# Description: 生成类似lfw的评估数据
import os
import shutil
from PIL import Image
import random


def rename_and_resize(data_dir, save_dir, resize_img=None):
    """
    重命名与尺寸调整
    :param data_dir:
    :param save_dir:
    :param resize_img:
    :return:
    """
    original_path = data_dir
    saved_path = save_dir
    make_path(saved_path)
    all_folders = traversalDir_FirstDir(original_path)
    for folder in all_folders:
        files = os.listdir(os.path.join(original_path, folder))
        i = 1
        for file in files:
            suffix = '.png'
            name = folder + '_' + str(i).zfill(4) + suffix
            i = i + 1
            sub_saved_path = os.path.join(saved_path, folder)
            original_file_path = os.path.join(original_path, folder) + '/' + file
            make_path(sub_saved_path)
            if resize_img is not None:
                resize_img(original_file_path, sub_saved_path + '/' + file, int(resize_img))
            else:
                shutil.copyfile(original_file_path, sub_saved_path + '/' + name)


# To get all sub folders in one folder
def traversalDir_FirstDir(path):
    list = []
    if (os.path.exists(path)):
        files = os.listdir(path)
        for file in files:
            m = os.path.join(path,file)
            if (os.path.isdir(m)):
                h = os.path.split(m)
                list.append(h[1])
        return list


# To judge whether a folder is existed.
def make_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def resize(image_path, saved_path, size):
    img = Image.open(image_path)
    img = img.resize((size, size), Image.ANTIALIAS)
    img.save(saved_path)


class GeneratePairs:
    """
    Generate the pairs.txt file for applying "validate on LFW" on your own datasets.
    """

    def __init__(self, data_dir, repeat_times=100):
        """
        Parameter data_dir, is your data directory.
        Parameter pairs_filepath, where is the pairs.txt that belongs to.
        Parameter img_ext, is the image data extension for all of your image data.
        """
        self.data_dir = data_dir
        self.pairs_filepath = data_dir + '/pairs.txt'
        self.repeat_times = int(repeat_times)
        self.img_ext = '.png'

    def generate(self):
        # The repeate times. You can edit this number by yourself
        folder_number = self.get_folder_numbers()
        print('共'+str(folder_number)+'个文件夹')
        # This step will generate the hearder for pair_list.txt, which contains
        # the number of classes and the repeate times of generate the pair
        if not os.path.exists(self.pairs_filepath):
            with open(self.pairs_filepath,"a") as f:
                f.write(str(self.repeat_times) + "\t" + str(folder_number) + "\n")
        for i in range(self.repeat_times):
            self._generate_matches_pairs()
            self._generate_mismatches_pairs()

    def get_folder_numbers(self):
        count = 0
        for folder in os.listdir(self.data_dir):
            if os.path.isdir(os.path.join(self.data_dir, folder)):
                count += 1
        return count

    def _generate_matches_pairs(self):
        """
        Generate all matches pairs
        """
        for name in os.listdir(self.data_dir):
            if not os.path.isdir(os.path.join(self.data_dir, name)):
                continue

            a = []
            for file in os.listdir(os.path.join(self.data_dir, name)):
                if file == ".DS_Store":
                    continue
                a.append(file)

            with open(self.pairs_filepath, "a") as f:
                temp = random.choice(a).split("_") # This line may vary depending on how your images are named.
                w = temp[0]
                l = random.choice(a).split("_")[1].lstrip("0").rstrip(self.img_ext)
                r = random.choice(a).split("_")[1].lstrip("0").rstrip(self.img_ext)
                f.write(w + "\t" + l + "\t" + r + "\n")

    def _generate_mismatches_pairs(self):
        """
        Generate all mismatches pairs
        """
        for i, name in enumerate(os.listdir(self.data_dir)):
            if not os.path.isdir(os.path.join(self.data_dir, name)):
                continue

            remaining = os.listdir(self.data_dir)

            del remaining[i]
            remaining_remove_txt = remaining[:]
            for item in remaining:
                if not os.path.isdir(os.path.join(self.data_dir, item)):
                    remaining_remove_txt.remove(item)

            remaining = remaining_remove_txt

            other_dir = random.choice(remaining)
            with open(self.pairs_filepath, "a") as f:
                    file1 = random.choice(os.listdir(os.path.join(self.data_dir, name)))
                    file2 = random.choice(os.listdir(os.path.join(self.data_dir, other_dir)))
                    f.write(name + "\t" + file1.split("_")[1].lstrip("0").rstrip(self.img_ext) \
                     + "\t" + other_dir + "\t" + file2.split("_")[1].lstrip("0").rstrip(self.img_ext) + "\n")


if __name__ == '__main__':
    data_dir = '/Users/zhousf/tensorflow/zhousf/data/test'
    save_dir = '/Users/zhousf/tensorflow/zhousf/data/test-deal'
    rename_and_resize(data_dir=data_dir, save_dir=save_dir)
    generatePairs = GeneratePairs(data_dir=save_dir)
    generatePairs.generate()