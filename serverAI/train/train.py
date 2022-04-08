import os
import numpy as np
from config import *
import tensorflow as tf

from model import MDF_Model
from tensorflow.keras.applications import vgg16, resnet_v2, inception_v3, inception_resnet_v2
from preprocess import *
from dataset import *

train_file_lists = [os.listdir(os.path.join(TRAIN_DIR, i))  for i in CLASS_NAMES]
test_file_lists = [os.listdir(os.path.join(VAL_DIR, i))  for i in CLASS_NAMES]

train_dataset = (
    tf.data.Dataset.from_generator(
        train_data_generator, 
        # output_types = [tf.float32, tf.float32],
        # output_shapes = [tf.TensorShape([IMG_SIZE[0], IMG_SIZE[1], 3]), tf.TensorShape([])]
        output_signature = (
            tf.TensorSpec(shape=(IMG_SIZE[0],IMG_SIZE[1], 3), dtype=tf.float32), 
            tf.TensorSpec(shape=(), dtype=tf.float32,)  
        )
    )
    .shuffle(BUFFER_SIZE)
    .batch(BATCH_SIZE, drop_remainder=True)
    .prefetch(tf.data.experimental.AUTOTUNE)
)

# test_dataset = (
#     tf.data.Dataset.from_generator(
#         test_data_generator,
#         output_signature = (
#             tf.TensorSpec(shape=(IMG_SIZE[0], IMG_SIZE[1], 3), dtype=tf.float32), 
#             tf.TensorSpec(shape=(), dtype=tf.float32)  
#         )
#     )
#     .shuffle(BUFFER_SIZE)
#     .batch(BATCH_SIZE, drop_remainder=True)
#     .prefetch(tf.data.experimental.AUTOTUNE)
# )




# model = MDF_Model()
# model.summary()