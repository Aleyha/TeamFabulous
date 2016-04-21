'''
 Main program for FART (test)

 This program talks to the server backend and line detection

 Tells the line program to start and stop. It also sends the station name

 Tells the server backend if the line detection started and sends the station name to the main program
'''
import zmq

context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.setsockopt(zmq.IDENTITY, b'main')
socket.connect('tcp://localhost:5559')


