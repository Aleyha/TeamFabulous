#!/usr/bin/python

# Import modules for CGI handling
import cgi, cgitb

form = cgi.FieldStorage()

if form.getvalue('station'):
    station = form.getvalue('station')
else:
    station = "not entered"
    
print "Content-type:text/html\r\n\r\n"
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<title>Sending Message</title>"
print "</head>"
print "<body>"
print "<p>hello you chose station %s</p>" %station
print "<?php echo 'WHAT THE FUCK' ?>"
print "</body>"
print "</html>"