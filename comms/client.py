# Simple request-reply broker
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

# ROUTER is the requester
# ROUTER sends a command to the motor 'worker'

import zmq
from random import randint
import sys

# Prepare our context and sockets
context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.setsockopt(zmq.IDENTITY, b'line')
socket.connect('tcp://localhost:5559')


# Initialize poll set
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
#  counter = 0;
while True:
    msg = input("enter message: ")
    
    socket.send_multipart([b'motor', str(msg)])
    
    print "polling for a message"
    sockets = dict(poller.poll(1000))
    if socket in sockets:
        print socket.recv_multipart()
    
   



socket.close()