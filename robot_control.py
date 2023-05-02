#!/usr/bin/python3

import os, sys
import time
import robot_server 
import serial
from camera import Camera
import threading

if __name__ == '__main__':
    server_thread = threading.Thread(target = robot_server.start_server)
    server_thread.start()
    device = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.1)

    while not robot_server.get_ready():
        print("not ready")
        time.sleep(0.2)
    print('system on! Press CTRL-C to exit')
    while True:
        left = robot_server.get_left_message()
        right = robot_server.get_right_message()
        forward = robot_server.get_forward_message()
        backward = robot_server.get_backward_message()

        command = 4
        if (forward == "forward pressed"):
            command = 0
        elif (backward == "backward pressed"):
            command = 1
        elif (left == "left pressed"):
            command = 2
        elif (right == "right pressed"):
            command = 3
        if (command != 4):
            print(command)
        device.write(str(command).encode())
        time.sleep(0.1)