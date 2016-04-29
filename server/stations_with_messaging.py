#!/usr/bin/python

# Import modules for CGI handling
import cgi, cgitb
import zmq


# get the station name from the POST form data
form = cgi.FieldStorage()

if form.getvalue('station'):
    station = form.getvalue('station').upper()
else: 
    station = None

# must create the zmq context before creating a socket
context = zmq.Context()

# setting up socket for communication with the main program
socket = context.socket(zmq.DEALER)
socket.setsockopt(zmq.IDENTITY, b'server')
socket.connect('tcp://localhost:5550')

# set up object that looks for reponse messages
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

# send station to main program to start the line detection
socket.send_multipart([station])

timeout = False
# wait for 1 second for a response
sockets = dict(poller.poll(1000))
if socket in sockets: # save the response which means line detection started
    msg = socket.recv_multipart()
else: # no response
    timeout = True

socket.close()
 
print "Content-type:text/html\r\n\r\n"
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<title>Dropdown Box - Sixth CGI Program</title>"
print "</head>"
print "<body>"

print "<h2>"
if timeout:
    print "robot is busy"
else:
    print msg
print "</h2>"
    
print "</body>"
print "</html>"
