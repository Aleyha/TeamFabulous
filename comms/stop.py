
# DEALER is the worker
# DEALER receives a command to execute
# motor connection

import zmq
import serial
import traceback
from time import sleep


#ser = serial.Serial('COM8', 9600) # Establish the connection on a specific port
ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port
for i in range(0, 10):
	ser.write(b'0') # Convert the decimal number to ASCII then send it to the Arduino
sleep(.1) # Delay for one tenth of a second#print ser.readline() #Read the newest output from the Arduino

		    

