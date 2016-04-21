'''
SERVER SIDE ZMQ CODE
'''

import zmq

context = zmq.Context()

# setting up socket for communication with the main program
socket = context.socket(zmq.ROUTER)
socket.setsockopt(zmq.IDENTITY, b'server')
socket.connect('tcp://localhost:5550')

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

while True:
    print "sending a message"
    station = raw_input("what station? ")
    socket.send_multipart([b'main',b'server', station])
    
    print "polling for a message"
    sockets = dict(poller.poll(1000))
    if socket in sockets:
        print socket.recv_multipart()
    else:
        print "timeout; no message sent!"
   

socket.close()
