
# DEALER is the worker
# DEALER receives a command to execute
# motor connection

import zmq
from time import sleep
import serial
import traceback


try:


	#ser = serial.Serial('COM8', 9600) # Establish the connection on a specific port
	ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port

	while True:
	    message = raw_input("what command, fam? ") 
	    print message
	    ser.write(str(message)) # Convert the decimal number to ASCII then send it to the Arduino
	    sleep(.1) # Delay for one tenth of a second
	    #print ser.readline() #Read the newest output from the Arduino

		    

except Exception as e:
	trace =  traceback.format_exc()
	print trace
	f = open("/home/fart/TeamFabulous/comms/motor.txt", "w")
	#traceback.print_stack(e)
	f.write(trace)
	f.close()
	time.sleep(300)
