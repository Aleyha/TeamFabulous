
# DEALER is the worker
# DEALER receives a command to execute
# Sends back the status of motors...?

import zmq
from time import sleep
import serial


context = zmq.Context()
socket = context.socket(zmq.DEALER)
socket.setsockopt(zmq.IDENTITY, b'motor')
socket.bind("tcp://*:5559")


ser = serial.Serial('COM8', 9600) # Establish the connection on a specific port

while True:
    counter = socket.recv()
    print "recieved: " + counter
    ser.write(str(counter)) # Convert the decimal number to ASCII then send it to the Arduino
    #socket.send_multipart([b'line',ser.readline()]) # Read the newest output from the Arduino
    #sleep(.1) # Delay for one tenth of a second

            
