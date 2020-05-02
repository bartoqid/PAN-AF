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
  <title>Software Versions</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>
<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    Software Versions
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

print '<div class="response">'
#Get firewall software version info
cmd = "<request><system><software><check></check></software></system></request>"
tree = fwCmd(cmd)
print "PAN-OS<br>"
print "<table cellpadding=5 cellspacing=0 border=1>"
print "<tr>"
print '<td width="100px" align="center">Version</td>'
print '<td align="center">Released</td>'
print '<td width="100px" align="center">Downloaded</td>'
print '<td width="100px" align="center">Current</td>'
print '<td width="100px" align="center">Latest</td>'
print "</tr>"
for entry in tree.findall('./result/sw-updates/versions/entry'):
  if (
    entry.find('downloaded').text == "yes" or
    entry.find('current').text == "yes" or
    entry.find('latest').text == "yes"
    ):
    print "<tr>"
    print '<td align="center">%s</td>' % (entry.find('version').text, )
    print "<td>%s</td>" % (entry.find('released-on').text, )
    print '<td align="center">%s</td>' % (entry.find('downloaded').text, )
    print '<td align="center">%s</td>' % (entry.find('current').text, )
    print '<td align="center">%s</td>' % (entry.find('latest').text, )
    print "</tr>"
print "</table>"
print "<br><br>"
cmd="<request><content><upgrade><check></check></upgrade></content></request>"
tree = fwCmd(cmd)
print "Dynamic Updates<br>"
print "<table cellpadding=5 cellspacing=0 border=1>"
print "<tr>"
print '<td width="100px" align="center">Version</td>'
print '<td align="center">Released</td>'
print '<td width="100px" align="center">Downloaded</td>'
print '<td width="100px" align="center">Current</td>'
print '<td width="100px" align="center">Previous</td>'
print '<td width="100px" align="center">Installing</td>'
print '<td width="100px" align="center">Features</td>'
print '<td width="100px" align="center">Update Type</td>'
print "</tr>"
for entry in tree.findall('./result/content-updates/entry'):
  if (
    entry.find('downloaded').text == "yes" or
    entry.find('current').text == "yes" or
    entry.find('previous').text == "yes" or
    entry.find('installing').text == "yes"
    ):
    print "<tr>"
    print '<td align="center">%s</td>' % (entry.find('version').text, )
    print "<td>%s</td>" % (entry.find('released-on').text, )
    print '<td align="center">%s</td>' % (entry.find('downloaded').text, )
    print '<td align="center">%s</td>' % (entry.find('current').text, )
    print '<td align="center">%s</td>' % (entry.find('previous').text, )
    print '<td align="center">%s</td>' % (entry.find('installing').text, )
    print '<td align="center">%s</td>' % (entry.find('features').text, )
    print '<td align="center">%s</td>' % (entry.find('update-type').text, )
    print "</tr>"
print "</div>"
print "</body>"
print "</html>"
