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
  <title>DHCP Utilization</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>
<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    DHCP Utilization
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

print '<div class="response">'

values = {'type': 'op', 'cmd': '<show><dhcp><server><lease><show-expired>no</show-expired><interface>all</interface></lease></server></dhcp></show>', 'key': fwkey}
palocall = 'https://%s/api/' % (fwhost)
r = requests.post(palocall, data=values, verify=False)

print("<table cellpadding=2 cellspacing=0 border=1>")
print("<tr><td>Interface</td><td>Allocated</td><td>Total</td><td>%</td></tr>")

dhcptree = ET.fromstring(r.text)
for interface in dhcptree.findall('./result/interface'):
  name = interface.get('name')
  allocated = interface.get('allocated')
  total = interface.get('total')
  if int(allocated) != 0:
    percent = str(int((float(allocated)/float(total))*100))
  else:
    percent = "0"
  print("<tr><td>%s</td><td>%s</td><td>%s</td>" % (name, allocated, total))
  if (int(percent) > 89):
    print('<td><font color="red">%s</font></td></tr>' % (percent, ))
  elif (int(percent) > 79):
    print('<td><font color="orange">%s</font></td></tr>' % (percent, ))
  else:
    print('<td>%s</td></tr>' % (percent, ))
print("</table>")

print "</div>"


print """
  </body>
  </html>
"""
