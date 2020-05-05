#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(format='text')  # for troubleshooting
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET

bpatokenfile = "/var/dug/bpatokenfile.py"

print "Content-type: text/html"
print

print """
<html>
<head>
  <title>BPA Token</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>
<body>
<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    Generate Key
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

form = cgi.FieldStorage()
bpatoken = form.getvalue("bpatoken")

if bpatoken:
    file = open(bpatokenfile, "w")
    line = 'bpatoken = "%s"\n' % (bpatoken, )
    file.write(line)
    file.close()

    print '<div class="response">'
    print "<br>\n"
    print "Successfully written BPA Token to the credential store."

else:
    print """
<div class="form1">
  <form method="post" action="/cgi-bin/bpatoken.cgi">
    <label>Enter BPA Token</label><br>
    <input type="text" name="bpatoken"/><br>
    <input type="submit" value="Submit"/>
  </form>
</div>
</body>
</html>
  """