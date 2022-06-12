import json
import logging
import math
import cv2
import sys, os
PYTHONPATH=os.getcwd() + '/Modules'
sys.path.append(PYTHONPATH)
import userconfig

class frame_process:

    id_video_frame=0
    total_frames = 0
    fps = 0
    frame_size =0 
    video_writer = ''
    capture_obj=''
    source_type=''
    source_path=''

    manual_fps = userconfig.MANUAL_FPS
    seconds = userconfig.LIMIT_TOSECONDS_PERFRAME
    try_attemp = userconfig.ATTEMPT_CAMERA

    # Discontinuous mode
    # Video
    list_frames_tostore = []
    # Video-stream
    f_discontinous_mode = False

    def __init__(self,src_type,src_path) -> None:

        if(self.seconds > 0):
            self.f_discontinous_mode = True

        self.source_path = src_path
        self.source_type = src_type

        if (src_path.isnumeric()):
            src_path = int(src_path)

        self.capture_obj = cv2.VideoCapture(src_path)
        self.fps = int(self.capture_obj.get(cv2.CAP_PROP_FPS))
        self.total_frames = self.capture_obj.get(cv2.CAP_PROP_FRAME_COUNT)
        self.frame_size =(int(self.capture_obj.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self.capture_obj.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fps_towritevideo = self.fps

        if(self.f_discontinous_mode == True):
            if(self.seconds <= 0):
                self.seconds = 1
            number_frames_tosave = math.floor(self.total_frames / (self.fps*self.seconds))+1
            save_frame=[None]*number_frames_tosave
            self.list_frames_tostore = [ (self.fps*self.seconds)*i+1 for i,frame in enumerate(save_frame)]
            fps_towritevideo = 1/self.seconds

        if(self.manual_fps > 0):
            fps_towritevideo = self.manual_fps

        if(self.source_type == "VIDEO" or self.source_type == "STREAM"):
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter('outTemp/output.avi', fourcc, fps_towritevideo, self.frame_size)

    def video_processing(self):
        status=0

        rev, frame = self.capture_obj.read()
        if not rev:
            logging.error("Error to read frame")
            status=1

        self.id_video_frame+=1
        #logging.debug("Frame %d/%d", self.id_video_frame,self.total_frames)

        return status, frame

    def stream_proccesing(self):

        status = 0
        try_attempt =0

        while(try_attempt <= (self.try_attemp-1)):

            try_attempt += 1

            if not self.capture_obj.isOpened():
                logging.debug("There is no communication with the camera")
                status = 1

            logging.debug("Capturing frame...")
            frame_grabbed, frame = self.capture_obj.read()

            if not frame_grabbed:
                logging.debug("Frame could not be captured")
                status = 1

            # Error, Reconnect camera
            if status != 0:
                logging.debug("Reset camera")
            #OK, status =0
            else:
                logging.debug("Frame Captured.")
                
                return status, frame
        #Error
        return status, frame

    def read_frame(self):
        status=0
        frame_raw=""

        # From imagen or video
        if(self.source_type == "IMAGE"):
            #logging.debug("Image frame")
            try:
                frame_raw = cv2.imread(self.source_path)
            except:
                logging.error("Could not read image source")
                status=1

        # From Camera
        if(self.source_type == "VIDEO"):
            #logging.debug("Video frame")

            try:
                status, frame_raw = self.video_processing()
                if(status == 0 and self.f_discontinous_mode == True):
                    keepthisframe_status=1
                    for frame_tostore in self.list_frames_tostore:
                        if(self.id_video_frame == frame_tostore):
                            keepthisframe_status=0  
                            break
                    status=keepthisframe_status
            except:
                logging.error("Could not read video source")
                status=1

        if(self.source_type == "STREAM"):
            #logging.debug("Streaming frame")

            try:
                status, frame_raw = self.stream_proccesing()
            except:
                logging.error("Could not read stream source")
                status=1
        
        # Reescale
        rescale_str=userconfig.RESIZE_FRAME.replace("(", "").replace(")", "")
        tuple_resize = tuple(map(int, rescale_str.split(',')))
        if (tuple_resize != (0,0)):
            frame_raw = cv2.resize(frame_raw, tuple_resize, interpolation= cv2.INTER_LINEAR)

        return status, frame_raw