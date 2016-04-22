'''
 Main program for FART (test)

 This program talks to the server backend and line detection

 Tells the line program to start and stop. It also sends the station name

 Tells the server backend if the line detection started and sends the station name to the main program
'''

import zmq
import subprocess

context = zmq.Context()

# creating a socket for the line detection
# and server to talk to
socket = context.socket(zmq.DEALER)
socket.setsockopt(zmq.IDENTITY, b'main')
socket.bind('tcp://*:5550')


# Initialize poll set
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

while True:
    print "recieving message"
    ident, msg = socket.recv_multipart()
    if ident == "server":
        socket.send_multipart([b'server', b'bet'])
        subprocess.call(["python", "/home/christie/TeamFabulous/lineDetection/line-detection-red.py", msg])
        socket.send_multipart([b'server', b'K'])
     
        
  

socket.close()