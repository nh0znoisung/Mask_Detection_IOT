import os
from config import *
import tensorflow as tf
import argparse
import pickle

from model import MDF_Model
from preprocess import *
from dataset import *
from metrics import *
from time import time

from callbacks import F1History
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy


parser = argparse.ArgumentParser()
parser.add_argument('--train_dir', dest='train_dir', type=str,
    help='train directory', default=None)
parser.add_argument('--val_dir', dest='val_dir', type=str,
    help='validation directory', default=None)
parser.add_argument('--backbone', dest='backbone', type=str,
    help='model backbone, feasible values are \
        [vgg16,ResNet50V2,inception_v3, inception_resnet_v2]', 
    default=None)
args = parser.parse_args()

if args.train_dir:
    if os.path.isdir(args.train_dir): TRAIN_DIR = args.train_dir
    else:
        print(f"Error: {args.train_dir} is not a folder.")
        exit()
if args.val_dir:
    if os.path.isdir(args.val_dir): VAL_DIR = args.val_dir
    else:
        print(f"Error: {args.val_dir} is not a folder.")
        exit()
if args.backbone:
    if args.backbone not in FEASIBLE_BACKBONE:
        print(f"Error: {args.backbone} is not a feasible backbone.")
        exit()
    else: BACKBONE = args.backbone


def main():
    start = time()

    train_file_lists =  [ 
        [
            os.path.join(TRAIN_DIR, i, os.path.join(j, k))
            for j in os.listdir(os.path.join(TRAIN_DIR, i))  
            for k in os.listdir(os.path.join(TRAIN_DIR, i, j))
            if os.path.isdir(os.path.join(TRAIN_DIR, i, j))
        ]   
        for i in CLASS_NAMES
    ]

    test_file_lists =  [ 
        [   
            os.path.join(VAL_DIR, i, os.path.join(j, k))
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
        .batch(BATCH_SIZE, drop_remainder=False)
        .prefetch(tf.data.experimental.AUTOTUNE)
    )

    test_dataset = (
        tf.data.Dataset.from_generator(
            test_data_generator(1, test_file_lists, max_it=None),
            output_signature = (
                tf.TensorSpec(shape=(IMG_SIZE[0], IMG_SIZE[1], 3), dtype=tf.float32), 
                tf.TensorSpec(shape=(), dtype=tf.float32)  
            )
        )
        .batch(BATCH_SIZE, drop_remainder=False)
        .prefetch(tf.data.experimental.AUTOTUNE)
    )


    print(f"COMPLETE PREPARING DATASET IN {time()-start}s.")
    start=time()

    model = MDF_Model()
    model.build(input_shape = (None, IMG_SIZE[0], IMG_SIZE[1], 3) )
    model.summary()
    model.compile(optimizer=Adam(LR),
                loss = BinaryCrossentropy(), 
                # metrics = ['accuracy', precision_m, recall_m, f1_m]
                )
    
    ckpt_dir = f'./ckpts/{BACKBONE}'
    
    if not os.path.isdir(ckpt_dir):
        os.makedirs(ckpt_dir)
    
    model_checkpoint_callback=tf.keras.callbacks.ModelCheckpoint(
        ckpt_dir,
        monitor='val_f1',
        verbose=1,
        save_best_only=True,
        save_weights_only=False,
        mode='max',
        save_freq='epoch',
    )
    
    callback_his = F1History(test_dataset)
    history = model.fit(train_dataset,
        validation_data=test_dataset,
        steps_per_epoch=STEPS_PER_EPOCH,
        epochs=EPOCHS,
        verbose=1,
        callbacks=[callback_his, model_checkpoint_callback]
    )
    
    print(f"DONE TRAINING MODEL IN {time()-start}s.")
    
    history_name = f'history.pkl'
    pickle.dump(callback_his.history, open(os.path.join(ckpt_dir, history_name), 'wb'))

if __name__ == "__main__":
    main()