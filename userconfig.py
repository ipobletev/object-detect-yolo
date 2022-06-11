import os
from dotenv import load_dotenv
load_dotenv()

#Use .env file and add useful macros

################################################################ 
################################ USEFUL CONFIG
################################################################ 

# Frame type
# IMAGE, VIDEO, STREAM
SOURCE_TYPE = os.getenv('SOURCE_TYPE', 'IMAGE')

# Just for realtime FRAME_TYPE="DYNAMIC", attempting to reconnect tries.
ATTEMPT_CAMERA = int(os.getenv('ATTEMPT_CAMERA', '3'))

# Sensor path or dir to the source of frame
SOURCE_PATH = os.getenv('SENSOR_PATH', 'inTemp/image.jpg')

# Enable for save image from yolo processing to /outTemp
ENABLE_WRITE_FRAME = (os.getenv('ENABLE_WRITE_FRAME', 'False') == 'True')

# Enable show GUI for each frame, just for machine with desktop os.
VM_GUI = (os.getenv('VM_GUI', 'False') == 'True')

# Enable save log to folder /log
ENABLE_LOG_FILE=(os.getenv('ENABLE_LOG_FILE', 'False') == 'True')

################################################################ 
################################ YOLO CONFIG
################################################################ 

# Yolo processing size
YOLO_WIDTH_IMAGE_SIZE = int(os.getenv('YOLO_WIDTH_IMAGE_SIZE', '320'))
YOLO_HEIGHT_IMAGE_SIZE = int(os.getenv('YOLO_HEIGHT_IMAGE_SIZE', '320'))

# Yolo supression for NMS Non-Maximun Suppression
# Low value, minor mount of detect bounding box from 1 object
# High value, mayor mount of detext bounding box of 1 object
YOLO_SUPRESSION = float(os.getenv('YOLO_SUPRESSION', '0.4'))

# Yolo filter for detection
# Low value, more detection, but low probability to detect real object
# High value, fewer detections, but high probability to detect real object
YOLO_THRESHOLD = float(os.getenv('YOLO_THRESHOLD', '0.6'))

# Use for other yolo weight
YOLO_WEIGHT_PATH = os.getenv('YOLO_WEIGHT_PATH', 'dnn_model/yolov3.weights')
YOLO_WEIGHT_CFG_PATH = os.getenv('YOLO_WEIGHT_CFG_PATH', 'dnn_model/yolov3.cfg')

# Store names clases for model
# Base classes to compare with USER_CLASSES_PATH
CLASSES_PATH = os.getenv('CLASSES_PATH', 'dnn_model/coco.names')
# Classes for user. Modify it with class type to detect only these classes.
USER_CLASSES_PATH = os.getenv('USER_CLASSES_PATH', 'dnn_model/classes.txt')
