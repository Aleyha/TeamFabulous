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

def exit_program(socket):
    # socket.send_multipart([b'main', b'line' b'stopped'])
    exit(0)

station = sys.argv[1]
print "starting line detection with station " + station
    
# Prepare our context and sockets
context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.setsockopt(zmq.IDENTITY, b'line')
socket.connect('tcp://localhost:5559')

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
        exit_program(main_socket)
    
    socket.send_multipart([b'motor', str(msg)])
    
    print "polling for a message"
    sockets = dict(poller.poll(1000))
    if socket in sockets:
        print socket.recv_multipart()

    
   

socket.close()