import time
import cv2
import os, glob
import sys
import userconfig
import logging
from threading import Timer
from datetime import datetime, timezone
PYTHONPATH=os.getcwd() + '/Modules'
sys.path.append(PYTHONPATH)
from SME_ImageProcessing import ImageProcessing
from download_yolomodel import attempt_download_cfg, attempt_download_weigth

def camera_process(camera_path):

    status = 0
    try_attempt =0

    while(try_attempt <= (userconfig.ATTEMPT_CAMERAS-1)):

        try_attempt += 1
        capture_obj = cv2.VideoCapture(camera_path)

        if not capture_obj.isOpened():
            logging.debug("No hay comunicacion con la camara")
            status = 1

        logging.debug("Capturando frame...")
        frame_grabbed, frame = capture_obj.read()

        if not frame_grabbed:
            logging.debug("No se pudo capturar frame")
            status = 1

        # Error, Reconnect camera
        if status != 0:
            logging.debug("Reinicializo camara")
        #OK, status =0
        else:
            logging.debug("Capturado.")
            return status, frame
    #Error
    return status, frame

def main_program():

    # if camera is gone - Reinitialize camera conectivity
    logging.debug("---------------------------------------------")

    # Read frame
    status=0
    frame=""
    frame_raw=""

    # From imagen or video
    if(userconfig.FRAME_TYPE == "STATIC"):
        logging.debug("Static frame")
        try:
            frame_raw = cv2.imread(userconfig.SENSOR_PATH)
        except:
            logging.error("No se pudo leer fuente static")
            status=1

    # From Camera
    if(userconfig.FRAME_TYPE == "DYNAMIC"):
        logging.debug("Dynamic frame")
        try:
            status, frame_raw = camera_process(userconfig.SENSOR_PATH)
        except:
            logging.error("No se pudo leer frame")
            status=1

    # Analize image
    if status == 0:
        frame = frame_raw.copy()
        # Analize the image frame
        flag_detection= False
        flag_detection, objects_detected = yolobject.YoloProcessing(frame)

        if flag_detection == True:
            pass

    # Stop image
    if(userconfig.VM_GUI == True):
        if(cv2.waitKey(1) == 27):
            pass

    # Show image debug
    if(userconfig.VM_GUI == True):
        cv2.imshow('YOLO Algorithm', frame)
    
    # Write processed imagen 
    if(userconfig.ENABLE_WRITE_FRAME == True):
        cv2.imwrite("outTemp/"+ str(datetime.now()) + ".png", frame)

if __name__ == '__main__':
    # Clear terminal
    clear = lambda: os.system('clear')
    clear()

    # Delete temp image and jsondata
    for filename in glob.glob("outTemp/temp_*"):
        os.remove(filename)

    # Init debug
    if userconfig.ENABLE_LOG_FILE == True:
        logging.basicConfig(
            level=logging.DEBUG,
            format='[%(levelname)s] - %(asctime)s %(threadName)-10s: %(message)s',
            handlers=[
                logging.FileHandler("log/ova-lascondes_" + str(datetime.now()) + ".log"),
                logging.StreamHandler()
            ]
            )
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format='[%(levelname)s] - %(asctime)s %(threadName)-10s: %(message)s'
            )

    logging.debug("###################################")
    logging.debug("Inicializa sistema")
    logging.debug("###################################")

    # Init Neuronal Network with yolo
    logging.debug(os.path.basename(userconfig.YOLO_WEIGHT_PATH))
    attempt_download_weigth(userconfig.YOLO_WEIGHT_PATH)
    attempt_download_cfg(userconfig.YOLO_WEIGHT_CFG_PATH)
    yolobject = ImageProcessing(userconfig.YOLO_WEIGHT_CFG_PATH,userconfig.YOLO_WEIGHT_PATH)

    while(1):
        try:

            main_program()
            break

        except KeyboardInterrupt:
            # Control + C (Remote)
            logging.debug("key stop")
            break
        # except Exception as error_info:
        #     logging.error("Un error ha ocurrido.")
        #     logging.debug(error_info)
        #     break

    logging.debug("###################################")
    if(userconfig.VM_GUI == True):
        cv2.destroyAllWindows()

    #video_capture.release()
    logging.debug("Sistema Finalizado")
    logging.debug("###################################")
    logging.debug("###################################")
