import cv2
from threading import Thread
import time
import numpy as np

class WebcamVideoStream:
    def __init__(self, src = 0):
        print("init")
        self.stream = cv2.VideoCapture(0, cv2.CAP_V4L)
#         (self.grabbed, self.frame) = self.stream.read()
#         self.stopped = False
#         time.sleep(2.0)
    
#     def start(self):
#         print("start thread")
#         t = Thread(target=self.update, args=())
#         t.daemon = True
#         t.start()
#         return self
#     
#     def update(self):
#         print("read")
#         while (self.stream.isOpened()):
#             if self.stopped:
#                 return
#             
#             (self.grabbed, self.frame) = self.stream.read()
#     
#     def read(self):
#         return self.frame
#     
#     def stop(self):
#         self.stopped = True
        
    def __del__(self):
        self.stream.release()
        
    def get_frame(self):
        ret, frame = self.stream.read()
        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

