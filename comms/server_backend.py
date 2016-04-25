'''
SERVER SIDE ZMQ CODE
'''

import zmq

context = zmq.Context()

# setting up socket for communication with the main program
socket = context.socket(zmq.DEALER)
socket.setsockopt(zmq.IDENTITY, b'server')
socket.connect('tcp://localhost:5550')

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

station = raw_input("what station? ")

socket.send_multipart([station])
print "polling for a message"
timeout = False
sockets = dict(poller.poll(1000))
if socket in sockets:
    print socket.recv_multipart()
else:
    timeout = True
    print "timeout"
  
socket.close()
