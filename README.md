# Object Detector Yolo-OpenCV

Object detection with yolo-opencv.

## Instalation
```
pip3 install -U -r requirements.txt
```

## Run program with test image

Weight and cfg files will be downloaded by default to yolov3 with the program is execute.\
classes.txt file have car and person, just this two classes will be detected \
Run program. It use the test image "image.jpg" from inTemp folder.
```
python3 main.py
```
Program will download the weight and cfg file by defaul from https://pjreddie.com/darknet/yolo/ if it is not present in dnn_folder.


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
  
## Configuration
If you need use other weight or others class-object detection, do the following:
#### 1-If need to change the source (image, video, camera,etc) use the macro:
For image and video \
FRAME_TYPE = 'STATIC' (Default)\
SENSOR_PATH = 'inTemp/image.jpg'(Default)\
For stream and cameras:\
FRAME_TYPE = 'DYNAMIC'\
SENSOR_PATH = 'path'\
ATTEMPT_CAMERA = 3(Default)

#### 2-For change threshold or supression for NMS change the macro:
YOLO_THRESHOLD = 0.6(Default)\
YOLO_SUPRESSION = 0.4(Default)

#### 3-For add or delete classes.
Edit dnn_folder/classes.txt (user class to detect). Add the classes names to detect. (By default just car and person are in the file). It is compare with coco.names.\
If you need to change the path. Use the following macros and make a .env file in main folder:\
CLASSES_PATH='dnn_model/coco.names'\
USER_CLASSES_PATH='dnn_model/classes.txt'

#### 4-For use other weight and cfg files.
Use dnn_folder to keep cfg and weight files (Default: yolov3). It is downloaded automaticaly by default.\
If you need to change the path. Use the following macros and make a .env file in main folder:\
YOLO_WEIGHT_PATH='dnn_model/yolov3.weights'\
YOLO_WEIGHT_CFG_PATH='dnn_model/yolov3.cfg'

#### 5-Use other useful enviroment macros

## About Enviroment macros
Make a .env file and use some macros, which has the following default value:

### Useful macros

Frame type: STATIC/DYNAMIC \
STATIC: Images and video. \
DYNAMIC: Realtime stream - camera
```
FRAME_TYPE = 'STATIC'
```
Just for realtime and represent the attempting to reconnect tries (with FRAME_TYPE="DYNAMIC").
```
ATTEMPT_CAMERA = 3
```
Sensor path or dir to the source frame. Change to video o other path.
```
SENSOR_PATH = 'inTemp/image.jpg'
```
Save image after yolo processing to outTemp
```
ENABLE_WRITE_FRAME = False
```
Show GUI for each frame, just for machine with desktop os.
```
VM_GUI = False
```
Save log file to folder /log
```
ENABLE_LOG_FILE = False
```

### YOLO CONFIG


Yolo processing size
```
YOLO_WIDTH_IMAGE_SIZE = 320
YOLO_HEIGHT_IMAGE_SIZE = 320
```
Yolo supression for NMS Non-Maximun Suppression
Low value, minor mount of detect bounding box from 1 object
High value, mayor mount of detext bounding box of 1 object
```
YOLO_SUPRESSION = 0.4
```
Yolo filter for detection
Low value, more detection, but low probability to detect real object
High value, fewer detections, but high probability to detect real object
```
YOLO_THRESHOLD = 0.6
```
Use for other yolo weight
```
YOLO_WEIGHT_PATH = dnn_model/yolov3.weights
```
```
YOLO_WEIGHT_CFG_PATH = dnn_model/yolov3.cfg
```
Store names clases for model
Base classes to compare with USER_CLASSES_PATH
```
CLASSES_PATH = dnn_model/coco.names
```
Classes for user. Modify it with class type to detect only these classes.
```
USER_CLASSES_PATH = dnn_model/classes.txt
```
