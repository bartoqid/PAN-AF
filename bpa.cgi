#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(format='text')  # for troubleshooting
import sys

print "Content-type: text/html"
print

print """
<html>
<head>
  <title>BPA Automation</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>
<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    BPA Automation
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

print """
<div class="form1">
  <form method="post" action="/cgi-bin/downloadbpa.cgi">
    <label>Do you want to generate BPA Report?<br>
     Please make sure you have enter the BPA Token.<br> 
     Press submit to continue. This process will take awhile. Please be patient.</label><br>
    <input type="submit" value="Submit"/>
  </form>
</div>
</body>
</html>
  """
print "</div>"
print "</body>"
print "</html>"
