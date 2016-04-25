# Simple request-reply broker
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

# ROUTER is the requester
# ROUTER sends a command to the motor 'worker'

# this will emmulate the line detection code
# the line detection does not need to tell the main program to start or stop
# only tells it errors

import zmq
import sys
import time
#station = sys.argv[1]
#print "starting line detection with station " + station
    
def line_detection(socket):
    for i in range(4):
        for i in range(4):
            print "sleeping"
            time.sleep(1)
            socket.send_multipart([b'motor', str(i)])

    
# Prepare our socket to talk to the motor
context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.setsockopt(zmq.IDENTITY, b'line')
socket.connect('tcp://localhost:5559')


# prepare socket that talks to the main program
main_socket = context.socket(zmq.DEALER)
main_socket.setsockopt(zmq.IDENTITY, b'line')
main_socket.connect('tcp://localhost:5550')

# Initialize poll set
#poller = zmq.Poller()
#poller.register(socket, zmq.POLLIN)

while True:
    print "waiting for message..."
    print main_socket.recv_multipart()
    print "running line detection"
    line_detection(socket)
    print "sending a message to main"
    main_socket.send_multipart([b"finished"])


socket.close()
main_socket.close()