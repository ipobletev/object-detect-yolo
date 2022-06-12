# Object Detector Yolo-OpenCV

Object detection with yolo-opencv. Image, video file and streaming camera features.

## Instalation
```
pip3 install -U -r requirements.txt
```

## Run program with test image

Weight and cfg files will be downloaded by default (yolov3) when main.py program is executed.\
By default just two classes will be detected, if you want more modified and add it in classes.txt file \
Run the default program will use the test image "image.jpg" from inTemp folder.
```
python3 main.py
```
Program will download the weight and cfg file by defaul (yolov3) from https://pjreddie.com/darknet/yolo/ if it is not present in dnn_folder.


## About Tree Folder
    .
    ├── dnn_model                 # Folder with weight, cfg files and classes details for user.
    │   ├──classes.txt            # File with the user class names to use (default just = car, person)
    │   ├──coco.names             # File with all classes to support
    │   ├──yolo_x.cfg             # cfg yolo file for weight (default=yolov3.cfg, will be downloaded by main.py)
    │   ├──yolo_x.weight          # weight yolo file (default=yolov3.weights, will be downloaded by main.py)
    ├── inTemp                    # Keep test image and video
    ├── log                       # Save log of program (if ENABLE_LOG_FILE=True)
    ├── Modules                   # Libraries
    ├── outTemp                   # Save frame image after yolo processing (if ENABLE_WRITE_FRAME=True)
    ├── main.py                   # Yolo main program
    ├── userconfig.py             # Contain macros linked to a .env file
    ├── requirements.txt          # Dependencies to install 
    └── README.md

## Configure and macros
#### 0- Add or ignore classes.
Edit dnn_folder/classes.txt for user class to detect. Add the classes names to detect. (By default just car and person are in the file). It is compare with coco.names. If you need to change the path, use the following macros and make a .env file in main folder:
```
CLASSES_PATH='dnn_model/coco.names'
USER_CLASSES_PATH='dnn_model/classes.txt'
```
#### 1- Set source path and type of source. Image (Default), video, camera stream:
For image ('IMAGE'), video file ('VIDEO') and camera stream ('STREAM').
```
SOURCE_TYPE = 'IMAGE'
SENSOR_PATH = 'inTemp/image.jpg'
```
#### 2- Configure yolo cfg, weight path and config threshold or supression:
```
YOLO_WEIGHT_CFG_PATH="dnn_model/yolov3.cfg"
YOLO_WEIGHT_PATH="dnn_model/yolov3.weights"
YOLO_THRESHOLD = 0.6
YOLO_SUPRESSION = 0.4
```
#### 3- Use other useful enviroment macros
Activate the GUI and show image frame
```
VM_GUI = True
```
Write output file
```
ENABLE_WRITE_FRAME=True
```
Resize input frame
```
RESIZE_FRAME = (1000,500)
```
Limit. How seconds for each frame (video and stream). Default value = 0 without limit.
```
LIMIT_TOSECONDS_PERFRAME=5
```
Save log file to folder "log"
```
ENABLE_LOG_FILE = False
```
For streaming camera, numbers of try to reconnect and acquire frame.
```
ATTEMPT_CAMERA = 3
```
## Examples uses
Image file source, uso yolov3, show the result per frame and save the Image result.
```
# 1- Source
SOURCE_PATH = 'inTemp/test-image.jpg'
SOURCE_TYPE = 'IMAGE'

# 2- Configure Model
YOLO_WEIGHT_CFG_PATH="dnn_model/yolov3.cfg"
YOLO_WEIGHT_PATH="dnn_model/yolov3.weights"
YOLO_SUPRESSION = 0.4
YOLO_THRESHOLD = 0.6

# 3-Other Macros
# VM GUI
VM_GUI = True

# Write Output file
ENABLE_WRITE_FRAME=True
```
Video file source, uso yolov3, show the result per frame and save the video result.
```
# 1- Source
SOURCE_PATH = 'inTemp/test-video.mp4'
SOURCE_TYPE = 'VIDEO'

# 2- Configure Model
YOLO_WEIGHT_CFG_PATH="dnn_model/yolov3.cfg"
YOLO_WEIGHT_PATH="dnn_model/yolov3.weights"
YOLO_SUPRESSION = 0.4
YOLO_THRESHOLD = 0.6

# 3-Other Macros
# VM GUI
VM_GUI = True

# Write Output file
ENABLE_WRITE_FRAME=True
```
Stream camera source, uso yolov3, show the stream result per frame.
```
# 1- Source
SOURCE_PATH = 0
SOURCE_TYPE = 'STREAM'

# 2- Configure Model
YOLO_WEIGHT_CFG_PATH="dnn_model/yolov3.cfg"
YOLO_WEIGHT_PATH="dnn_model/yolov3.weights"
YOLO_SUPRESSION = 0.4
YOLO_THRESHOLD = 0.6

# Other Macros
# VM GUI
VM_GUI = True
```
Stream camera source, uso yolov3, show the stream result per frame and use limit frame each 5 seconds and save it into a video file.
```
# 1- Source
SOURCE_PATH = 0
SOURCE_TYPE = 'STREAM'

# 2- Configure Model
YOLO_WEIGHT_CFG_PATH="dnn_model/yolov3.cfg"
YOLO_WEIGHT_PATH="dnn_model/yolov3.weights"
YOLO_SUPRESSION = 0.4
YOLO_THRESHOLD = 0.6

# 3-Other Macros
# Limit. How seconds for each frame. Default value = 0 without limit.
LIMIT_TOSECONDS_PERFRAME = 5

# Write Output file
ENABLE_WRITE_FRAME=True

# VM GUI
VM_GUI = True
```
