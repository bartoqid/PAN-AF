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
  <title>DHCP Leases</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>
<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    DHCP Leases
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

print '<div class="response">'

values = {'type': 'op', 'cmd': '<clear><user-cache><all></all></user-cache></clear>', 'key': fwkey}
palocall = 'https://%s/api/' % (fwhost)
r = requests.post(palocall, data=values, verify=False)
tree = ET.fromstring(r.text)
print "Clear user mappings from the data plane: %s<br>" % (tree.get("status"), )


values = {'type': 'op', 'cmd': '<clear><user-cache-mp><all></all></user-cache-mp></clear>', 'key': fwkey}
palocall = 'https://%s/api/' % (fwhost)
r = requests.post(palocall, data=values, verify=False)
tree = ET.fromstring(r.text)
print "Clear user mappings from the management plane: %s" % (tree.get("status"), )

print "</div>"
print "</body>"
print "</html>"
