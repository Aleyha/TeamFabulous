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
line_detection_in_use = False
while True:

    
    station = raw_input("what station? ")
    if line_detection_in_use:
        print "line detection in use"
        
        print "polling for a message"
        sockets = dict(poller.poll(1000))
        if socket in sockets:
            print socket.recv_multipart()
            line_detection_in_use = False
            
    if not line_detection_in_use:
        socket.send_multipart([b'main',b'server', station])
        print socket.recv_multipart()
        line_detection_in_use = True

   

socket.close()
