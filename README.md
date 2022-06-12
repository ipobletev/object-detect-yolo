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

## Examples uses


## Configuration
If you need use other weight or others class-object detection, do the following:
#### 1-Change the frame source and path. Image (Default), video, camera:
For image ('IMAGE'), video file ('VIDEO') and stream camera ('STREAM').
```
SOURCE_TYPE = 'IMAGE'
SENSOR_PATH = 'inTemp/image.jpg'
```
#### 2-Configure yolo cfg, weight path and config threshold or supression:
```
YOLO_WEIGHT_CFG_PATH="dnn_model/yolov3.cfg"
YOLO_WEIGHT_PATH="dnn_model/yolov3.weights"
YOLO_THRESHOLD = 0.6
YOLO_SUPRESSION = 0.4
```
#### 3-For add or ignore classes.
Edit dnn_folder/classes.txt for user class to detect. Add the classes names to detect. (By default just car and person are in the file). It is compare with coco.names.\
If you need to change the path, use the following macros and make a .env file in main folder:\
```
CLASSES_PATH='dnn_model/coco.names'
USER_CLASSES_PATH='dnn_model/classes.txt'
```
#### 4-Use other useful enviroment macros
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
For streaming camera, try to reconnect and acquire frame.
```
ATTEMPT_CAMERA = 3
```
