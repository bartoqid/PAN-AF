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
  <title>ARP Entries</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>
<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    ARP Entries
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

print '<div class="response">'

values = {'type': 'op', 'cmd': '<show><arp><entry name ="all"/></arp></show>', 'key': fwkey}
palocall = 'https://%s/api/' % (fwhost)
r = requests.post(palocall, data=values, verify=False)
arptree = ET.fromstring(r.text)
if (arptree.get('status') == "success"):
  for entries in arptree.findall('./result/entries'):
    print '<table cellpadding=5 cellspacing=0 border=1>'
    print '<tr><td>IP</td><td>MAC</td><td>Status</td><td>TTL</td><td>Interface</td><td>Port</td></tr>'
    for entry in entries.findall('entry'):
      print "<tr>"
      print "<td>%s</td>" % (entry.find('ip').text, )
      print "<td>%s</td>" % (entry.find('mac').text, )
      print "<td>%s</td>" % (entry.find('status').text, )
      print "<td>%s</td>" % (entry.find('ttl').text, )
      print "<td>%s</td>" % (entry.find('interface').text, )
      print "<td>%s</td>" % (entry.find('port').text, )
      print "</tr>"
    print "</table>"

print "</div>"


print """
  </body>
  </html>
"""
