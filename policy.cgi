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

def testPolicy(fwhost, fwkey, sourcezone, sourceip, destzone, destip, destport, application, protocol):
  type = "op"
  cmd = "<test>"
  cmd += "<security-policy-match>"
  cmd += "<from>%s</from>" % (sourcezone, )
  cmd += "<source>%s</source>" % (sourceip, )
  cmd += "<to>%s</to>" % (destzone, )
  cmd += "<destination>%s</destination>" % (destip, )
  cmd += "<destination-port>%s</destination-port>" % (destport, )
  cmd += "<application>%s</application>" % (application, )
  cmd += "<protocol>%s</protocol>" % (protocol, )
  cmd += "</security-policy-match>"
  cmd += "</test>"
  values = {'type': type, 'cmd': cmd, 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  r = requests.post(palocall, data=values, verify=False)
  ruletree = ET.fromstring(r.text.replace("(", "").replace(")", ""))
  rules = ruletree.findall('./result/rules/entry')
  if rules is not None:
    print "The requested traffic matches on the following policies:<br>"
    for rule in rules:
      print "%s: %s<br>" % (rule.find('action').text, rule.get('name'))
  else:
    print "The requested traffic does not currently match any rules in the policy."

def getZones(fwhost, fwkey):
  zones = []
  type = "config"
  action = "get"
  xpath = "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/zone"
  values = {'type': type, 'action': action, 'xpath': xpath, 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  r = requests.post(palocall, data=values, verify=False)
  tree = ET.fromstring(r.text)
  for entries in tree.findall('./result/zone'):
    for entry in entries.findall('entry'):
      zones.append(entry.get('name'))
  return zones

def getApplications(fwhost, fwkey):
  applications = []
  type = "config"
  action = "get"
  xpath = "/config/predefined/application"
  values = {'type': type, 'action': action, 'xpath': xpath, 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  r = requests.post(palocall, data=values, verify=False)
  tree = ET.fromstring(r.text.encode('ascii', 'ignore'))
  for entries in tree.findall('./result/application'):
    for entry in entries.findall('entry'):
      applications.append(entry.get('name'))
  return applications

print "Content-type: text/html"
print

print """
<html>
<head>
  <title>Test Security Policy</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>
<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    Test Security Policy
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

#Check to see if we received posted variables
form = cgi.FieldStorage()
sourcezone = form.getvalue("sourcezone")
sourceip = form.getvalue("sourceip")
destzone = form.getvalue("destzone")
destip = form.getvalue("destip")
destport = form.getvalue("destport")
application = form.getvalue("application")
protocol = form.getvalue("protocol")

if (sourcezone and sourceip and destzone and destip and destport and application and protocol):
  print '<div class="response">'
  testPolicy(fwhost, fwkey, sourcezone, sourceip, destzone, destip, destport, application, protocol)
  print "</div>"

else:
#  zones = []
#  applications = []
  zones = getZones(fwhost, fwkey)
  applications = getApplications(fwhost, fwkey)

  print '<div class="form1">'
  print '  <form method="post" action="/cgi-bin/policy.cgi">'
  print '    <label>Source Zone</label><br>'
  print '      <select name="sourcezone"/>'
  for zone in zones:
    print '      <option value="%s">%s</option>' % (zone, zone)
  print '      </select></br>'
  print '    <label>Source IP</label><br>'
  print '    <input type="text" name="sourceip"/><br>'
  print '    <label>Destination Zone</label><br>'
  print '    <select name="destzone"/>'
  for zone in zones:
    print '      <option value="%s">%s</option>' % (zone, zone)
  print '    </select></br>'
  print '    <label>Destination IP</label><br>'
  print '    <input type="text" name="destip"/><br>'
  print '    <label>Destination Port</label><br>'
  print '    <input type="text" name="destport"/><br>'
  print '    <label>Application</label><br>'
  print '    <select name="application"/>'
  for application in applications:
    print '        <option value="%s">%s</option>' % (application, application)
  print '    </select></br>'
  print '    <label>Protocol</label><br>'
  print '    <select name="protocol"/>'
  print '      <option value="6">TCP</option>'
  print '      <option value="17">UDP</option>'
  print '    </select><br>'
  print '    <input type="submit" value="Submit"/>'
  print '  </form>'
  print '</div>'

print """
  </body>
  </html>
"""
