#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(format='text')  # for troubleshooting
import sys
import time
import urllib
import requests
import datetime
import json 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET


print "Content-type: text/html"
print

print """
<html>
<head>
  <title>Clear User-IP Mapping</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>
<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    Clear User-IP Mapping
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line


print """
<div class="form1">
  <form method="post" action="/cgi-bin/clearusers.cgi">
    <label>Are you sure you want to clear User-IP mapping?<br>
     Press submit to continue
    <br><br>
    </label><br>
    <input type="submit" value="Submit"/>
  </form>
</div>
</body>
</html>
  """

print "</div>"
print "</body>"
print "</html>"
