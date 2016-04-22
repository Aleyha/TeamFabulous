#!/usr/bin/python

# Import modules for CGI handling
import cgi, cgitb
import zmq

form = cgi.FieldStorage()

if form.getvalue('dropdown'):
    station = form.getvalue('dropdown')
else:
    station = "not entered"
    exit(0)
    
socket = context.socket(zmq.ROUTER)
socket.setsockopt(zmq.IDENTITY, b'server')
socket.connect('tcp://localhost:5550')

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

socket.send_multipart([b'main',b'server', station])
timeout = True
sockets = dict(poller.poll(1000))
if socket in sockets:
    socket.recv_multipart()
    timeout = False

print "Content-type:text/html\r\n\r\n"
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<title>Dropdown Box - Sixth CGI Program</title>"
print "</head>"
print "<body>"
if timeout:
    print "<p>Robot is busy</p>"
else:
    print "<p>You chose station %s</p>" % station
print "</body>"
print "</html>"