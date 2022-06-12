from random import randint
from click import Path
import cv2
import numpy as np
import userconfig
import logging

# Class for processing a frame and send that image with multiples multiples json detected objects.
class ImageProcessing():

    #Neuronal Network
    neural_network = ""

    #Object Detection Parameters
    threshold = userconfig.YOLO_THRESHOLD
    suppresion = userconfig.YOLO_SUPRESSION
    yolo_imagesize_width = userconfig.YOLO_WIDTH_IMAGE_SIZE
    yolo_imagesize_height = userconfig.YOLO_HEIGHT_IMAGE_SIZE
    original_width=0
    original_height=0

    # Load classes data
    classes_yolo = []
    user_classes_yolo = []

    # Initialice neuronal network
    def __init__(self, cfg_path, weights_path):

        # Load Network
        self.neural_network = cv2.dnn.readNet(cfg_path, weights_path)

        # Setup yolo weights and cfg
        self.neural_network = cv2.dnn.readNetFromDarknet(cfg_path, weights_path)

        # Define to run the algorithm with CPU
        self.neural_network.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.neural_network.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        self.classes = []
        self.load_class_names(userconfig.CLASSES_PATH,userconfig.USER_CLASSES_PATH)

    def load_class_names(self, classes_path="dnn_model/coco.names",classes_user_path="dnn_model/classes.txt"):

        # Store data classes for model
        with open(classes_path, "r") as file_classes:
            for count,file_class in enumerate(file_classes):
                raw_linetext = file_class.strip('\n')
                self.classes_yolo.append({})
                self.classes_yolo[count] = {
                    "class_id" : count,
                    "class_name" : raw_linetext,
                    "class_color" : (randint(0, 255), randint(0, 255), randint(0, 255))
                }

                #Manual color
                if(raw_linetext=="person"):
                    self.classes_yolo[count] = {
                        "class_id" : count,
                        "class_name" : raw_linetext,
                        "class_color" : (0,255,0)
                    }

                #Manual color
                if(raw_linetext=="car"):
                    self.classes_yolo[count] = {
                        "class_id" : count,
                        "class_name" : raw_linetext,
                        "class_color" : (255,0,0)
                    }

        # Store names user classes for model
        self.user_classes_yolo = []
        with open(classes_user_path, "r") as file_classes:
            for count,file_class in enumerate(file_classes):
                raw_linetext = file_class.strip('\n')
                self.user_classes_yolo.append(raw_linetext)

    # Main program to process image

    def YoloProcessing(self,in_frame):

        logging.debug("Se inicia el procesamiento de imagen. Parameters: %s - %s",
            str(self.threshold),str(self.suppresion))

        # Acquire original frame form image
        self.original_width, self.original_height = in_frame.shape[1], in_frame.shape[0]

        # Detect all objects
        output = self.detec_object(in_frame)

        # Filter by threshold and make a list objects
        list_objects = self.filter_objects(output)

        # Draw
        self.draw_detection(in_frame,list_objects)

        # Acquire number of deteccion
        number_deteccion = len(list_objects)

        # Print Finish process
        logging.debug("Finalizado. Total de Detecciones: %s", number_deteccion)
        if(number_deteccion > 0):
            # Print each data object
            for num,object in enumerate(list_objects):
                number_class_id = object[0]
                # Find the class name of object
                for i in range(len(self.classes_yolo)):
                    if(self.classes_yolo[i]["class_id"] == number_class_id):
                        name_class_id = self.classes_yolo[i]["class_name"]
                # Print data
                logging.debug("%d-Class: %s-%s", num+1,name_class_id,list_objects[num])
            return True, list_objects

        # Nothing detected
        return False, ''

    # Detect all objects
    def detec_object(self,in_frame):
        # the image into a BLOB [0-1] RGB - BGR
        blob = cv2.dnn.blobFromImage(in_frame, 1 / 255, (userconfig.YOLO_WIDTH_IMAGE_SIZE, userconfig.YOLO_HEIGHT_IMAGE_SIZE), True, crop=False)
        self.neural_network.setInput(blob)
        layer_names = self.neural_network.getLayerNames()
        # YOLO network has 3 output layer - note: these indexes are starting with 1
        output_names = [layer_names[i-1] for i in self.neural_network.getUnconnectedOutLayers()]
        outputs = self.neural_network.forward(output_names)
        return outputs

    # Filter just the interest object
    def filter_objects(self,model_outputs):
        boxes_relative = []
        boxes_absolute = []
        class_ids = []
        confidence_values = []
        list_objects = []

         #loop over each of the layer outputs
        for output in model_outputs:
            #for detection in output;
            for detection in output:
                #extract the class ID and confidence[i.e., probability)
                #of the current object detection
                scores = detection[5:]
                classid = np.argmax(scores)
                confidence = scores[classid]

                # Filter, find a valid object class name registered in classes.txt
                # Find de class_id object with database of yolo classes
                flag_valid_object=False
                for i in range(len(self.classes_yolo)):
                    if(self.classes_yolo[i]["class_id"] == classid):
                        # I have the class_name linked to the class_id
                        # print(CLASSES_YOLO[i]["class_name"])

                        # Check class_name object with classes.txt user file
                        for j in range(len(self.user_classes_yolo)):
                            if(self.classes_yolo[i]["class_name"] == self.user_classes_yolo[j]):
                                flag_valid_object=True
                                break
                
                # We have a valid object class name registered in classes.txt
                if(flag_valid_object==True):
                    # Filter by confidence threshold
                    if confidence > userconfig.YOLO_THRESHOLD:

                        # Bounding box relative coordenates
                        w, h = int(detection[2] * userconfig.YOLO_WIDTH_IMAGE_SIZE), int(detection[3] * userconfig.YOLO_HEIGHT_IMAGE_SIZE)
                        x, y = int(detection[0] * userconfig.YOLO_WIDTH_IMAGE_SIZE - w / 2), int(detection[1] * userconfig.YOLO_HEIGHT_IMAGE_SIZE - h / 2)
                        boxes_relative.append([x, y, w, h])
                        class_ids.append(classid)
                        confidence_values.append(float(confidence))

                        # Absolut coordenates to image frame
                        x = int(x * self.original_width /userconfig.YOLO_WIDTH_IMAGE_SIZE)
                        y = int(y * self.original_height/userconfig.YOLO_HEIGHT_IMAGE_SIZE)
                        w = int(w * self.original_width /userconfig.YOLO_WIDTH_IMAGE_SIZE)
                        h = int(h * self.original_height/userconfig.YOLO_HEIGHT_IMAGE_SIZE)
                        boxes_absolute.append([x, y, w, h])

        # Perform the non maximum suppression given the scores defined before
        # We going to calculate the number of detection "len(box_indexes_to_keep)" and the true id slots arrays of detections"
        box_indexes_to_keep = cv2.dnn.NMSBoxes(boxes_relative, confidence_values, userconfig.YOLO_THRESHOLD, userconfig.YOLO_SUPRESSION)

        # Filter with non maximum suppression results
        if(len(box_indexes_to_keep) > 0):
            for i in range(len(boxes_relative)):
                if i in box_indexes_to_keep:

                    # Write each detection data 
                    list_objects.append([class_ids[i], confidence_values[i], boxes_relative[i],boxes_absolute[i]])

        return list_objects

    def draw_detection(self,in_frame,list_objects):
        logging.debug("Draw roi")

        # Draw for each object
        for object in list_objects:
            # Acquire data from objects
            class_id=object[0]
            confidence=object[1]
            boundingbox_absolute = object[3]
            x,y,w,h = boundingbox_absolute

            # Find the class name of object 
            for i in range(len(self.classes_yolo)):
                if(self.classes_yolo[i]["class_id"] == class_id):
                    name_class_id = self.classes_yolo[i]["class_name"]
                    color_class_id = self.classes_yolo[i]["class_color"]

            # Draw process
            cv2.rectangle(in_frame, (x, y), (x+w, y+h), color_class_id, 2)
            #cv2.circle(img_withbox, (test_point[0],test_point[1]), 3, (255,0,0), 2)
            class_with_confidence = name_class_id + str(int(confidence * 100)) + '%'
            cv2.putText(in_frame, class_with_confidence, (x, y-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, color_class_id, 1)

        return in_frame