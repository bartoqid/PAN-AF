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

values = {'type': 'op', 'cmd': '<show><dhcp><server><lease><interface>all</interface></lease></server></dhcp></show>', 'key': fwkey}
palocall = 'https://%s/api/' % (fwhost)
r = requests.post(palocall, data=values, verify=False)

dhcptree = ET.fromstring(r.text)
print "<table cellpadding=5 cellspacing=0 border=1>"
print "<tr><td>IP</td><td>MAC</td><td>Hostname</td><td>State</td><td>Duration</td><td>Lease Time</td></tr>"
for lease in dhcptree.findall('./result/interface/entry'):
  print "<tr>"
  print "<td>%s</td>" % (lease.find('ip').text, )
  print "<td>%s</td>" % (lease.find('mac').text, )
  if lease.find('hostname') is not None:
    print "<td>%s</td>" % (lease.find('hostname').text, )
  else:
    print "<td></td>"
  if lease.find('state') is not None:
    print "<td>%s</td>" % (lease.find('state').text, )
  else:
    print "<td></td>"
  if lease.find('duration') is not None:
    print "<td>%s</td>" % (lease.find('duration').text, )
  else:
    print "<td></td>"
  if lease.find('leasetime') is not None:
    print "<td>%s</td>" % (lease.find('leasetime').text, )
  else:
    print "<td></td>"
  print "</tr>"
print "</table>"

print "</div>"


print """
  </body>
  </html>
"""
