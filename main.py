import time
import cv2
import os, glob
import sys
import userconfig
import logging
from datetime import datetime
PYTHONPATH=os.getcwd() + '/Modules'
sys.path.append(PYTHONPATH)
from SME_ImageProcessing import ImageProcessing
from download_yolomodel import attempt_download_cfg, attempt_download_weigth
from SME_frameProcess import frame_process

def image_processing():

    # Initial time
    last_time = time.time()
        
    logging.debug("---------------------------------------------")

    frame_status, frame_raw = frameprocess.read_frame()   

    if frame_status == 0 :
        
        ####################### Analize image #######################video_process
        frame_yolo = frame_raw.copy()

        # Analize the image frame
        flag_detection= False
        flag_detection, objects_detected = yolobject.YoloProcessing(frame_yolo)

        if flag_detection == True:
            pass

        ####################### Write to file #######################
        if(userconfig.ENABLE_WRITE_FRAME == True):
            # Write image
            cv2.imwrite("outTemp/"+ str(datetime.now()) + ".png", frame_yolo)
        
        ####################### Time #######################
        # Calculate FPS and finish time
        calculate_time = (time.time() - last_time)
        logging.debug("Time: %0.2f", calculate_time)
        last_time = time.time()

        ####################### Image GUI #######################
        if(userconfig.VM_GUI == True):
            while(1):
                cv2.imshow('YOLO Algorithm', frame_yolo)
                if(cv2.waitKey(1) == 27):
                    break

def video_processing():

    # Initial time
    last_time = time.time()

    while(1):
        
        ####################### Read frame in time #######################
        frame_status, frame_raw = frameprocess.read_frame()  

        if frame_status == 0:

            logging.debug("---------------------------------------------")

            ####################### Analize image #######################
            frame_yolo = frame_raw.copy()
            # Analize the image frame
            flag_detection= False
            flag_detection, objects_detected = yolobject.YoloProcessing(frame_yolo)

            if flag_detection == True:
                pass

            ####################### Write to file #######################
            if(userconfig.ENABLE_WRITE_FRAME == True):

                    frameprocess.video_writer.write(frame_yolo)

            ####################### Image GUI #######################
            if(userconfig.VM_GUI == True):
                cv2.imshow('YOLO Algorithm', frame_yolo)
                if(cv2.waitKey(1) == 27):
                    break
            
            ####################### FPS and time #######################
            if(userconfig.LIMIT_TOSECONDS_PERFRAME > 0):
                logging.debug("Frame: %s",frameprocess.id_video_frame)
            else:
                logging.debug("Frame: %s/%s",frameprocess.id_video_frame,frameprocess.total_frames)

            # Calculate FPS and finish time
            calculate_time = (time.time() - last_time)
            calculate_fps = (1.0 / calculate_time)
            time_left_min = int(calculate_time * (frameprocess.total_frames - frameprocess.id_video_frame))
            logging.debug("FPS: %0.2f - Time: %0.2f - TimeLeft: %0.2f [s]", calculate_fps, calculate_time,time_left_min)
            last_time = time.time()

        ####################### END #######################

        if(frameprocess.id_video_frame >= frameprocess.total_frames):
            frameprocess.capture_obj.release()
            frameprocess.video_writer.release()
            break

def stream_processing():

    # Initial time
    last_time = time.time()
    start_time = time.time() - userconfig.LIMIT_TOSECONDS_PERFRAME

    while(1):
        logging.debug("---------------------------------------------")

        ####################### Read frame in time #######################
        if(userconfig.LIMIT_TOSECONDS_PERFRAME > 0):
            frame_status, frame_raw = frameprocess.read_frame() 

        time_status=1
        if((time.time() - start_time) > userconfig.LIMIT_TOSECONDS_PERFRAME):
            # start time of the loop for limit functionality
            start_time = time.time() 

            if(userconfig.LIMIT_TOSECONDS_PERFRAME == 0):
                frame_status, frame_raw = frameprocess.read_frame()
            
            time_status=0

        if frame_status == 0 and time_status == 0:
            
            ####################### Analize image #######################
            frame_yolo = frame_raw.copy()
            # Analize the image frame
            flag_detection= False
            flag_detection, objects_detected = yolobject.YoloProcessing(frame_yolo)

            if flag_detection == True:


                
                pass

            ####################### Write to file #######################
            if(userconfig.ENABLE_WRITE_FRAME == True):
                frameprocess.video_writer.write(frame_yolo)
            
            ####################### FPS and time #######################
            # Calculate FPS and finish time
            calculate_time = (time.time() - last_time)
            calculate_fps = (1.0 / calculate_time)
            logging.debug("FPS: %0.2f - Time: %0.2f", calculate_fps, calculate_time)
            last_time = time.time()

        ####################### Image GUI #######################
        if(userconfig.VM_GUI == True):
            cv2.imshow('YOLO Algorithm', frame_yolo)
            if(cv2.waitKey(1) == 27):
                frameprocess.capture_obj.release()
                frameprocess.video_writer.release()
                break

if __name__ == '__main__':

    ################## INIT

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
                logging.FileHandler("log/log_" + str(datetime.now()) + ".log"),
                logging.StreamHandler()
            ]
            )
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format='[%(levelname)s] - %(asctime)s %(threadName)-10s: %(message)s'
            )

    logging.debug("###################################")
    logging.debug("Initialice System - Object Detector Yolo-OpenCV")
    logging.debug("###################################")

    #Init video process 
    frameprocess = frame_process(userconfig.SOURCE_TYPE, userconfig.SOURCE_PATH)

    # Download cfg and yolo weight
    logging.debug(os.path.basename(userconfig.YOLO_WEIGHT_PATH))

    if(userconfig.DISABLE_WEIGHT_DOWNLOAD == False):
        attempt_download_weigth(userconfig.YOLO_WEIGHT_PATH)
        attempt_download_cfg(userconfig.YOLO_WEIGHT_CFG_PATH)

    # Init Neuronal Network with yolo
    yolobject = ImageProcessing(userconfig.YOLO_WEIGHT_CFG_PATH,userconfig.YOLO_WEIGHT_PATH)

    ################## LOOP

    try:
        if(userconfig.SOURCE_TYPE == "IMAGE"):
            image_processing()
        if(userconfig.SOURCE_TYPE == "VIDEO"):
            video_processing()
        if(userconfig.SOURCE_TYPE == "STREAM"):
            stream_processing()

    except KeyboardInterrupt:
        # Control + C (Remote)
        logging.debug("key stop")
        if(userconfig.SOURCE_TYPE == "STREAM"):
            frameprocess.capture_obj.release()
            frameprocess.video_writer.release()
    # except Exception as error_info:
    #     logging.error("A error has ocurred.")
    #     logging.error(error_info)

    ################## END

    logging.debug("###################################")
    if(userconfig.VM_GUI == True):
        cv2.destroyAllWindows()

    #video_capture.release()
    logging.debug("System Finished")
    logging.debug("###################################")
    logging.debug("###################################")
