#!/usr/bin/python

# Import modules for CGI handling
import cgi, cgitb
import zmq

# get the station name from the form!
form = cgi.FieldStorage()

if form.getvalue('dropdown'):
    station = form.getvalue('dropdown').lower()
else:
    station = None

# create the zmq object
context = zmq.Context()

# setting up socket for communication with the main program
socket = context.socket(zmq.ROUTER)
socket.setsockopt(zmq.IDENTITY, b'server')
socket.connect('tcp://localhost:5550')

# setting up the recieving stuff
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

# checking whether we can call line detection or not
line_detection_in_use = False
if line_detection_in_use: # line detection is busy
    
    # polling for a message
    sockets = dict(poller.poll(1000))
    if socket in sockets:
    	# line detection is not busy if we recieve a message from main_program.py
    	# we will not save the message for now
    	# we only care that there is a message to recieve
        socket.recv_multipart() 
        line_detection_in_use = False
        
if not line_detection_in_use:
    socket.send_multipart([b'main',b'server', station])
    print socket.recv_multipart()
    line_detection_in_use = True

   

socket.close()

print "Content-type:text/html\r\n\r\n"
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<title>Dropdown Box - Sixth CGI Program</title>"
print "</head>"
print "<body>"
if line_detection_in_use:
    print "<p>Robot is busy</p>"
else:
    print "<p>You chose station %s</p>" % station
print "</body>"
print "</html>"