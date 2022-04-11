import os
from config import *
import tensorflow as tf
import argparse

from model import MDF_Model
from preprocess import *
from dataset import *
from metrics import *

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy

def main():

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

if __name__ == "__main__":

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
    
    main()