import tensorflow as tf
from config import *
from tensorflow.keras.applications import vgg16, resnet_v2, inception_v3, inception_resnet_v2
import tensorflow.keras.layers as layers

class MDF_Model(tf.keras.Model):
    def __init__(self):
        # Get backbone
        super().__init__()
        self.backbone = (
            vgg16.VGG16(weights="imagenet", input_shape=IMG_SIZE + (3,), include_top=False) if BACKBONE == 'vgg16'
            else resnet_v2.ResNet50V2(weights="imagenet", input_shape=IMG_SIZE + (3,), include_top=False) if BACKBONE == 'resnet50v2'
            else inception_v3.InceptionV3(weights="imagenet", input_shape=IMG_SIZE + (3,), include_top=False) if BACKBONE == 'inception_v3'
            else inception_resnet_v2.InceptionResNetV2(weights="imagenet", input_shape=IMG_SIZE + (3,), include_top=False)
        )
        self.pipeline = [
            layers.Flatten(),
            layers.Dense(512, activation="relu"),
            layers.BatchNormalization(),
            layers.Dense(256, activation="relu"),
            layers.BatchNormalization(),
            layers.Dense(1, activation='sigmoid')
        ]

        self.backbone.trainable = False
            
    def call(self, inputs, training=False): 
        x = inputs 

        x = self.backbone(x, training=False)
        for layer in self.pipeline:
            x = layer(x)
        
        return x