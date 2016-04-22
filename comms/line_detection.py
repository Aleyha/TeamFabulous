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


station = sys.argv[1]
print "starting line detection with station " + station
    
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
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

while True:

    msg = input("enter message: ")
    print msg
    if msg == 4:
        exit(0)
    
    socket.send_multipart([b'motor', str(msg)])
    
    print "sleeping"
    sockets = dict(poller.poll(1000))


    
   

socket.close()