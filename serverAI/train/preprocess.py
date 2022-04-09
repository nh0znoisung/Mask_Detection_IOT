from tensorflow.keras.applications import vgg16, resnet_v2, inception_v3, inception_resnet_v2
from config import *

def preprocess_image(image):
  if BACKBONE == 'vgg16':
    image = vgg16.preprocess_input(image)
  elif BACKBONE == 'ResNet50V2':
    image = resnet_v2.preprocess_input(image)
  elif BACKBONE == 'inception_v3':
    image = inception_v3.preprocess_input(image)
  elif BACKBONE == 'inception_resnet_v2':
    image = inception_resnet_v2.preprocess_input(image)
  return  image

def preprocess(images, labels):
  images = preprocess_image(images)
  return images, labels