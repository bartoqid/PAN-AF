#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(format='text')  # for troubleshooting
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET
sys.path.insert(0, '/var/dug/')
import fw_creds
fwhost = fw_creds.fwhost
fwkey = fw_creds.fwkey

print "Content-type: text/html"
print

print """
<html>
<head>
  <title>User-ID to Group Mappings</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>
<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    User-ID to Group Mappings
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

print '<div class="response">'

#Make call to firewall to get XML group mapping information
values = {'type': 'op', 'cmd': '<show><user><user-ids><all/></user-ids></user></show>', 'key': fwkey}
palocall = 'https://%s/api/' % (fwhost)
r = requests.post(palocall, data=values, verify=False)

#Convert the response from the firewall to an ElementTree to parse as XML
tree = ET.fromstring(r.text)

if (tree.get('status') == "success"):
  result = tree.find('result').text
  print "<table cellpadding=5 cellspacing=0 border=1>"
  print "<tr><td>User</td><td>Group</td></tr>"
  lines = result.split("\n")
  for line in lines:
    fields = line.split()
    if (len(fields) > 2) and (fields[0] <> "User") and (fields[0] <> "*"):
      print "<tr><td>%s</td><td>%s</td></tr>" % (fields[0], fields[2])
  print "</table>"

print "</div>"


print """
  </body>
  </html>
"""
