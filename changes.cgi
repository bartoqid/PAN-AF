#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(format='text')  # for troubleshooting

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET

import sys
sys.path.insert(0, '/var/dug/')
import fw_creds
fwhost = fw_creds.fwhost
fwkey = fw_creds.fwkey

from xmldiff import main, formatting
formatter = formatting.XMLFormatter()

print "Content-type: text/html"
print

print """
<html>
<head>
  <title>Pending Changes</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>
<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    Pending Changes
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

print('<div class="response"><pre>')

#Get running config
values = {'type': 'op', 'cmd': '<show><config><running/></config></show>', 'key': fwkey}
palocall = 'https://%s/api/' % (fwhost, )
try:
  response = requests.post(palocall, data=values, verify=False)
  tree = ET.fromstring(response.text)
  runningconfig = tree.find('./result/config')
except Exception as error:
  print(error)
  runningconfig = False

#Get candidate config
values = {'type': 'op', 'cmd': '<show><config><candidate/></config></show>', 'key': fwkey}
palocall = 'https://%s/api/' % (fwhost, )
try:
  response = requests.post(palocall, data=values, verify=False)
  tree = ET.fromstring(response.text)
  candidateconfig = tree.find('./result/config')
except Exception as error:
  print(error)
  candidateconfig = False

if runningconfig and candidateconfig:
  diffs = main.diff_texts(ET.tostring(runningconfig), ET.tostring(candidateconfig), formatter=formatter)
  for line in diffs.split("\n"):
    if "diff:" in line:
      print('<font color="red">%s</font>' % (line.replace("<", "&lt").replace(">", "&gt"), ))
    else:
      print(line.replace("<", "&lt").replace(">", "&gt"))

print('</pre>')
