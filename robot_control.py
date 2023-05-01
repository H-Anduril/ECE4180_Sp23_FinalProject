#!/usr/bin/python3

import os, sys
import time
import server 
# import serial
# from camera import Camera
import threading

if __name__ == '__main__':
	server_thread = threading.Thread(target = server.start_server)
	server_thread.start()
	device = serial.Serial(
		port='/dev/ttyACM0',
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=0.1)

	while not server.get_ready():
		print("not ready")
		time.sleep(0.2)
	print('system on! Press CTRL-C to exit')
	while True:
		left = server.get_left_message()
		right = server.get_right_message()
		forward = server.get_forward_message()
		backward = server.get_backward_message()

		command = -1
		if (forward == "forward pressed"):
			command = 0
		elif (backward == "backward pressed"):
			command = 1
		elif (left == "left pressed"):
			command = 2
		elif (right == "right pressed"):
			command = 3
		
		if (command != -1):
			print(command)
			device.write(comand.encode())
		time.sleep(0.1)