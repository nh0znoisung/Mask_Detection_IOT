import os
import numpy as np
from config import *
import tensorflow as tf

from model import MDF_Model
from preprocess import *
from dataset import *
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy

from keras import backend as K

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))



train_file_lists =  [ 
                        [
                            os.path.join(j, k) 
                            for j in os.listdir(os.path.join(TRAIN_DIR, i))  
                            for k in os.listdir(os.path.join(TRAIN_DIR, i, j))
                            if os.path.isdir(os.path.join(TRAIN_DIR, i, j))
                        ]   
                        for i in CLASS_NAMES
                    ]

test_file_lists =  [ 
                        [
                            os.path.join(j, k) 
                            for j in os.listdir(os.path.join(VAL_DIR, i))  
                            for k in os.listdir(os.path.join(VAL_DIR, i, j))
                            if os.path.isdir(os.path.join(VAL_DIR, i, j))
                        ]   
                        for i in CLASS_NAMES
                    ]

train_dataset = (
    tf.data.Dataset.from_generator(
        train_data_generator(1, train_file_lists), 
        # output_types = [tf.float32, tf.float32],
        # output_shapes = [tf.TensorShape([IMG_SIZE[0], IMG_SIZE[1], 3]), tf.TensorShape([])]
        output_signature = (
            tf.TensorSpec(shape=(IMG_SIZE[0],IMG_SIZE[1], 3), dtype=tf.float32), 
            tf.TensorSpec(shape=(), dtype=tf.float32,)  
        )
    )
    .batch(BATCH_SIZE, drop_remainder=True)
    .prefetch(tf.data.experimental.AUTOTUNE)
)

test_dataset = (
    tf.data.Dataset.from_generator(
        test_data_generator(1, test_file_lists),
        output_signature = (
            tf.TensorSpec(shape=(IMG_SIZE[0], IMG_SIZE[1], 3), dtype=tf.float32), 
            tf.TensorSpec(shape=(), dtype=tf.float32)  
        )
    )
    .batch(BATCH_SIZE, drop_remainder=True)
    .prefetch(tf.data.experimental.AUTOTUNE)
)


print("COMPLETE PREPARING DATASET.")

model = MDF_Model()
model.build(input_shape = (None, IMG_SIZE[0], IMG_SIZE[1], 3) )
model.summary()
model.compile(optimizer=Adam(LR),
              loss = BinaryCrossentropy(), 
              metrics = ['accuracy', precision_m, recall_m, f1_m])
history = model.fit(train_dataset,
                    validation_data=test_dataset,
                    steps_per_epoch=STEPS_PER_EPOCH,
                    epochs=EPOCHS,
                    verbose=1)