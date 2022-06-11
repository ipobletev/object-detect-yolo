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

class video_process:

    id_video_frame=0
    total_frames = 0
    fps = 0
    frame_size =0 
    video_writer = ''
    capture_obj=''

    def __init__(self,camera_path) -> None:
        
        if (camera_path.isnumeric()):
            camera_path = int(camera_path)

        self.capture_obj = cv2.VideoCapture(camera_path)
        self.fps = int(self.capture_obj.get(cv2.CAP_PROP_FPS))
        self.total_frames = self.capture_obj.get(cv2.CAP_PROP_FRAME_COUNT)
        self.frame_size =(int(self.capture_obj.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self.capture_obj.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        if(userconfig.MANUAL_FPS > 0):
            self.fps = userconfig.MANUAL_FPS

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video_writer = cv2.VideoWriter('outTemp/output.avi', fourcc, self.fps, self.frame_size)

    def video_processing(self):
        
        status=0

        rev, frame = self.capture_obj.read()
        if not rev:
            logging.error("Error to read frame")
            status=1

        self.id_video_frame+=1
        logging.debug("Frame %d/%d", self.id_video_frame,self.total_frames)

        return status, frame

    def stream_proccesing(self):

        status = 0
        try_attempt =0

        while(try_attempt <= (userconfig.ATTEMPT_CAMERA-1)):

            try_attempt += 1

            if not self.capture_obj.isOpened():
                logging.debug("No hay comunicacion con la camara")
                status = 1

            logging.debug("Capturando frame...")
            frame_grabbed, frame = self.capture_obj.read()

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

    # Initial time
    last_time = time.time()
    start_time = time.time() - userconfig.LIMIT_TOSECONDS_PERFRAME

    while(1):
        if((time.time() - start_time) > userconfig.LIMIT_TOSECONDS_PERFRAME):

            logging.debug("---------------------------------------------")
            # start time of the loop for limit functionality
            start_time = time.time() 

            ####################### Read frame #######################
            status=0
            frame_raw=""

            # From imagen or video
            if(userconfig.SOURCE_TYPE == "IMAGE"):
                logging.debug("Image frame")
                try:
                    frame_raw = cv2.imread(userconfig.SOURCE_PATH)
                except:
                    logging.error("No se pudo leer fuente de imagen")
                    status=1

            # From Camera
            if(userconfig.SOURCE_TYPE == "VIDEO"):
                logging.debug("Video frame")

                try:
                    status, frame_raw = videoprocess.video_processing()
                except:
                    logging.error("No se pudo leer fuente de video")
                    break

            if(userconfig.SOURCE_TYPE == "STREAM"):
                logging.debug("Streaming frame")

                try:
                    status, frame_raw = videoprocess.stream_proccesing()
                except:
                    logging.error("No se pudo leer fuente de stream")
                    break
  
            ####################### Analize image #######################
            if status == 0:

                frame_yolo = frame_raw.copy()
                # Analize the image frame
                flag_detection= False
                flag_detection, objects_detected = yolobject.YoloProcessing(frame_yolo)

                if flag_detection == True:
                    pass

                ####################### WRITE #######################
                if(userconfig.ENABLE_WRITE_FRAME == True):

                    # Write image
                    if(userconfig.SOURCE_TYPE == "IMAGE"):
                        cv2.imwrite("outTemp/"+ str(datetime.now()) + ".png", frame_yolo)
                    if(userconfig.SOURCE_TYPE == "VIDEO"):
                        videoprocess.video_writer.write(frame_yolo)
                    if(userconfig.SOURCE_TYPE == "STREAM"):
                        videoprocess.video_writer.write(frame_yolo)

                ####################### Image GUI #######################
                if(userconfig.VM_GUI == True):
                    cv2.imshow('YOLO Algorithm', frame_yolo)
                
                # Stop image
                if(userconfig.VM_GUI == True):
                    if(cv2.waitKey(1) == 27):
                        if(userconfig.SOURCE_TYPE == "STREAM"):
                            videoprocess.capture_obj.release()
                            videoprocess.video_writer.release()
                            break
            
            if(userconfig.SOURCE_TYPE == "IMAGE"):
                break

            if(userconfig.SOURCE_TYPE == "VIDEO"):
                if(videoprocess.id_video_frame >= videoprocess.total_frames):
                    videoprocess.capture_obj.release()
                    videoprocess.video_writer.release()
                    break
            
            # Calulate FPS and finish time
            calculate_time = (time.time() - last_time)
            calculate_fps = (1.0 / calculate_time)
            logging.debug("FPS: %0.2f - Time: %0.2f", calculate_fps, calculate_time)
            last_time = time.time()

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
    logging.debug("Inicializa sistema")
    logging.debug("###################################")

    #Init video process 
    if(userconfig.SOURCE_TYPE == "VIDEO" or userconfig.SOURCE_TYPE == "STREAM"):
        videoprocess = video_process(userconfig.SOURCE_PATH)

    # Download cfg and yolo weight
    logging.debug(os.path.basename(userconfig.YOLO_WEIGHT_PATH))

    if(userconfig.DISABLE_WEIGHT_DOWNLOAD == False):
        attempt_download_weigth(userconfig.YOLO_WEIGHT_PATH)
        attempt_download_cfg(userconfig.YOLO_WEIGHT_CFG_PATH)

    # Init Neuronal Network with yolo
    yolobject = ImageProcessing(userconfig.YOLO_WEIGHT_CFG_PATH,userconfig.YOLO_WEIGHT_PATH)

    ################## LOOP

    try:

        main_program()

    except KeyboardInterrupt:
        # Control + C (Remote)
        logging.debug("key stop")
        if(userconfig.SOURCE_TYPE == "STREAM"):
            videoprocess.capture_obj.release()
            videoprocess.video_writer.release()
    except Exception as error_info:
        logging.error("Un error ha ocurrido.")
        logging.error(error_info)

    ################## END

    logging.debug("###################################")
    if(userconfig.VM_GUI == True):
        cv2.destroyAllWindows()

    #video_capture.release()
    logging.debug("Sistema Finalizado")
    logging.debug("###################################")
    logging.debug("###################################")
