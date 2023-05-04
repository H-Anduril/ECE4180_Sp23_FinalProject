#!/usr/bin/python3

import os, sys
import time
import camera_server
# import serial
from camera import Camera
import threading

if __name__ == '__main__':
    server_thread = threading.Thread(target = camera_server.start_server)
    server_thread.start()


    while not camera_server.get_ready():
        print("not ready")
        time.sleep(0.2)
    print('system on! Press CTRL-C to exit')
    while True:
        time.sleep(0.3)