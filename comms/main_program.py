'''
 Main program for FART (test)

 This program talks to the server backend and line detection

 Tells the line program to start and stop. It also sends the station name

 Tells the server backend if the line detection started and sends the station name to the main program
'''

import zmq
import subprocess
import os

context = zmq.Context()

# creating a socket for the line detection
# and server to talk to
socket = context.socket(zmq.ROUTER)
socket.setsockopt(zmq.IDENTITY, b'main')
socket.bind('tcp://*:5550')


# Initialize poll set
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
line_detection_running= False
while True:
    print "recieving message"

    msg = socket.recv_multipart()
    print msg
    if msg[0] == "server":
        if not line_detection_running:
            socket.send_multipart([b'server', b'bet'])
            socket.send_multipart([b'line', b'start']) 

            line_detection_running = True
    if msg[0] == "line":
        print "assuming line is done..."
        line_detection_running = False
    

  

socket.close()