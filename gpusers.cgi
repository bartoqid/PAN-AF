#!/usr/bin/env python
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET
import datetime

import sys

sys.path.insert(0, '/var/dug/')

import fw_creds
fwhost = fw_creds.fwhost
fwkey = fw_creds.fwkey

fwhost = fw_creds.fwhost
fwkey = fw_creds.fwkey

def fwCmd(cmd):
  values = {'type': 'op', 'cmd': cmd, 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  try:
    r = requests.post(palocall, data=values, verify=False)
  except error as e:
    return false
  if r:
    tree = ET.fromstring(r.text)
    if tree.get('status') == "success":
      return tree
    else:
      return false



print "Content-type: text/html"
print

print """
<html>
<head>
  <title>GlobalProtect User Information</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>
<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    GlobalProtect User Information
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

print '<div class="response">'

cmd = "<show><global-protect-gateway><gateway><type>remote-user</type></gateway></global-protect-gateway></show>"
gwtree = fwCmd(cmd)

for entry in gwtree.findall('./result/entry'):
	cmd = "<show><global-protect-gateway><current-user><gateway>%s</gateway></current-user></global-protect-gateway></show>" % entry.find('gateway-name').text
	tree = fwCmd(cmd)
	print "Gateway Name : %s<br>" % (entry.find('gateway-name').text)
	print "<table cellpadding=5 cellspacing=0 border=1>"
	print "<tr>"
	print '<td width="100px" align="center">Username</td>'
	print '<td align="center">Region</td>'
	print '<td width="100px" align="center">Computer Name</td>'
	print '<td width="100px" align="center">Client OS</td>'
	print '<td width="100px" align="center">Virtual IP</td>'
	print '<td width="100px" align="center">Public IP</td>'
	print '<td width="100px" align="center">Tunnel Type</td>'
	print '<td width="100px" align="center">Login Time</td>'
	print '<td width="100px" align="center">Logout Time</td>'
	print "</tr>"
	for entry in tree.findall('./result/entry'):
    		print "<tr>"
    		print '<td align="center">%s</td>' % (entry.find('username').text, )
    		print "<td>%s</td>" % (entry.find('region-for-config').text, )
    		print '<td align="center">%s</td>' % (entry.find('computer').text, )
    		print '<td align="center">%s</td>' % (entry.find('client').text, )
    		print '<td align="center">%s</td>' % (entry.find('virtual-ip').text, )
    		print '<td align="center">%s</td>' % (entry.find('public-ip').text, )
    		print '<td align="center">%s</td>' % (entry.find('tunnel-type').text, )
    		print '<td align="center">%s</td>' % (entry.find('login-time').text, )
    		print '<td align="center">%s</td>' % (entry.find('logout-time').text, )
    		print "</tr>"
	print "</table>"
	print "<br><br>"

print "</div>"
print "</body>"
print "</html>"
