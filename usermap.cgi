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
  <title>IP to User-ID Mappings</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>
<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    IP to User-ID Mappings
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

print '<div class="response">'
#Make call to firewall to get XML user-id information
values = {'type': 'op', 'cmd': '<show><user><ip-user-mapping><all></all></ip-user-mapping></user></show>', 'key': fwkey}
palocall = 'https://%s/api/' % (fwhost)
r = requests.post(palocall, data=values, verify=False)

#Convert the response from the firewall to an ElementTree to parse as XML
tree = ET.fromstring(r.text)

if (tree.get('status') == "success"):
  print "<table cellpadding=5 cellspacing=0 border=1>"
  print "<tr><td>IP</td><td>User</td></tr>"
  for entry in tree.findall('./result/entry'):
    print "<tr>"
    print "<td>%s</td>" % (entry.find('ip').text, )
    print "<td>%s</td>" % (entry.find('user').text, )
    print "</tr>"
  print "</table>"
print "</div>"


print """
  </body>
  </html>
"""
