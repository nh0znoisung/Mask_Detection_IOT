### the generator will stop based all the number of data in pivot class
from config import *
from preprocess import *
import os
import numpy as np
import tensorflow as tf

def train_data_generator(pivot_class, file_lists):
    def f():
        n_class = len(CLASS_NAMES)
        permutation_lists = [np.random.choice(range(len(file_lists[i])), len(file_lists[pivot_class])) for i in range(n_class)]
        idx_list = [0]*n_class
        idx_class = 0
        while True:
            idx_file = permutation_lists[idx_class][ idx_list[idx_class] ]
            img_file_name = file_lists[idx_class][idx_file]
            img_path = os.path.join(TRAIN_DIR, CLASS_NAMES[idx_class], img_file_name)
            # print(img_path)
            img = tf.io.read_file(img_path)
            img = tf.image.decode_image(img, channels=3, expand_animations=False)
            img = tf.image.resize([img], IMG_SIZE)
            img, label = preprocess(img, idx_class)

            idx_list[idx_class] = (idx_list[idx_class]+1) % len(file_lists[idx_class])
            if idx_class==pivot_class and idx_list[idx_class]==0 and not loop_inf:
                break
            idx_class = (idx_class+1)%n_class

            yield img[0], label
    return f

### the generator will stop based all the number of data in pivot class
def test_data_generator(pivot_class, file_lists):
    def f():
        n_class = len(CLASS_NAMES)
        permutation_lists = [np.random.choice(range(len(file_lists[i])), len(file_lists[pivot_class])) for i in range(n_class)]
        idx_list = [0]*n_class
        idx_class = 0
        while True:
            idx_file = permutation_lists[idx_class][ idx_list[idx_class] ]
            img_file_name = file_lists[idx_class][idx_file]
            img_path = os.path.join(VAL_DIR, CLASS_NAMES[idx_class], img_file_name)
            img = tf.io.read_file(img_path)
            img = tf.image.decode_image(img, channels=3, expand_animations=False)
            img = tf.image.resize([img], IMG_SIZE)
            img, label = preprocess(img, idx_class)

            idx_list[idx_class] = (idx_list[idx_class]+1) % len(file_lists[idx_class])
            if idx_class==pivot_class and idx_list[idx_class]==0:
                break
            idx_class = (idx_class+1)%n_class

            yield img[0], label
    return f