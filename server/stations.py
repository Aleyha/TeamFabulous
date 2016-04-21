#!/usr/bin/python

# Import modules for CGI handling
import cgi, cgitb

form = cgi.FieldStorage()

if form.getvalue('dropdown'):
    station = form.getvalue('dropdown')
else:
    station = "not entered"
    
print "Content-type:text/html\r\n\r\n"
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<title>Dropdown Box - Sixth CGI Program</title>"
print "</head>"
print "<body>"
print "<p>hello you chose station %s</p>" %station
print "</body>"
print "</html>"