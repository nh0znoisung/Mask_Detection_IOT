# use one of: vgg16 ResNet50V2 inception_v3 inception_resnet_v2
FEASIBLE_BACKBONE = ['vgg16', 'resnet50v2', 'inception_v3', 'inception_resnet_v2']
BACKBONE = 'resnet50v2'    
IMG_SIZE = (224,224)

BATCH_SIZE = 128
LR = 2e-4
EPOCHS = 3
USE_AUGMENTATION = False
SEED = 10
STEPS_PER_EPOCH = None
TRAIN_DIR = 'data/RMFRD/train'
VAL_DIR = 'data/RMFRD/test'
MODEL_PATH = 'Model'
CLASS_NAMES = ['without_mask', 'with_mask']