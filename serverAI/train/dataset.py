### the generator will stop based all the number of data in pivot class
from config import *
from preprocess import *
import numpy as np
import tensorflow as tf

def train_data_generator(pivot_class, file_lists):
    def f():
        n_class = len(CLASS_NAMES)
        permutation_lists = [
            np.random.choice(range(len(file_lists[i])), len(file_lists[pivot_class])) 
            for i in range(n_class)]
        idx_list = [0]*n_class
        idx_class = 0
        while True:
            idx_file = permutation_lists[idx_class][ idx_list[idx_class] ]
            img_path = file_lists[idx_class][idx_file]

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

### the generator will stop based all the number of data in pivot class
def test_data_generator(pivot_class, file_lists, max_it=None):
    def f():
        n_class = len(CLASS_NAMES)
        permutation_lists = [
            np.random.choice(range(len(file_lists[i])), len(file_lists[i])) 
            for i in range(n_class)]
        idx_list = [0]*n_class
        idx_class = 0
        any_img_gen = False
        
        it=0
        
        while True:
            ### if over the list, not gen img
            if (idx_list[idx_class]+1) % (len(file_lists[idx_class])+1)==0:
                idx_class = (idx_class+1)%n_class
                if idx_class==0:
                    if not any_img_gen: break
                    any_img_gen=False
                continue
            
            any_img_gen=True
            
            idx_file = permutation_lists[idx_class][ idx_list[idx_class] ]
            img_path = file_lists[idx_class][idx_file]
            img = tf.io.read_file(img_path)
            img = tf.image.decode_image(img, channels=3, expand_animations=False)
            img = tf.image.resize([img], IMG_SIZE)
            img, label = preprocess(img, idx_class)

            idx_list[idx_class] = (idx_list[idx_class]+1) % len(file_lists[idx_class])
            if idx_list[idx_class] ==0: idx_list[idx_class]=len(file_lists[idx_class])
            idx_class = (idx_class+1)%n_class

            it += 1
            if max_it and it > max_it: break
            
            yield img[0], label

    return f