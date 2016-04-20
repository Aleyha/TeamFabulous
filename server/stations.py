#!/usr/bin/python

# Import modules for CGI handling
import cgi, cgitb

form = cgi.FieldStorage()

if form.getvalue('dropdown'):
    subject = form.getvalue('dropdown')
else:
    subject = "not entered"
    
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Dropdown Box - Sixth CGI Program</title>"
print "</head>"
print "<body>"
print "<h2> Selected Station is %s</h2>" % station
print "</body>"
print "</html>"