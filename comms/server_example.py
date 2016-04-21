# Simple request-reply broker
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

# DEALER is the worker
# DEALER receives a command to execute
# Sends back the status of motors...?

import zmq


# Prepare our context and sockets
context = zmq.Context()
socket = context.socket(zmq.DEALER)
socket.setsockopt(zmq.IDENTITY, b'motor')
socket.bind("tcp://*:5559")

# Initialize poll set
#poller = zmq.Poller()
#poller.register(socket, zmq.POLLIN)

while True:
    #print socket
    msg = socket.recv()
    print "recieved: " + msg
    
    if msg == '1':
        socket.send_multipart([b'line',b'driving motor'])
    else:
        socket.send(b'nothing')
    
    
socket.close()  

