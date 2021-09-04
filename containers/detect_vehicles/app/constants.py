import os

sep = os.path.sep

MODEL_DIR = f'{sep}smart-traffic{sep}model'

CFG_FILE_NAME = 'yolov4.cfg'
WEIGHTS_FILE_NAME = 'yolov4.weights'
CLASS_FILE_NAME = 'coco_classes.txt'

CFG_FILE_ABS_PATH = MODEL_DIR + sep + CFG_FILE_NAME
WEIGHTS_FILE_ABS_PATH = MODEL_DIR + sep + WEIGHTS_FILE_NAME
CLASS_FILE_ABS_PATH = MODEL_DIR + sep + CLASS_FILE_NAME

RESPONSE_HEADERS =  {
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}
