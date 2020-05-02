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

#These variables will change for each environment:
latitude = "39.938"
longitude = "-105.047"
natrule = "Outbound NAT"
securityrule = "Outbound - Unknown Device"

def getInterfaces(fwhost, fwkey):
  output = []
  values = {'type': 'op', 'cmd': '<show><interface>all</interface></show>', 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  r = requests.post(palocall, data=values, verify=False)
  tree = ET.fromstring(r.text)
  for entries in tree.findall('./result/hw'):
    for entry in entries.findall('entry'):
      info = {}
      info['name'] = entry.find('name').text
      output.append(info)
  return output

def createSubInterface(fwhost, fwkey, vlaninterface, vlannumber, vlannetwork, vlandescription):
  #Create the sub-interface
  print "Creating the sub-interface: "
  type = "config"
  action = "set"
  xpath = "/config/devices/entry[@name='localhost.localdomain']/network/interface/ethernet/entry[@name='%s']/layer3/units/entry[@name='%s.%s']" % (vlaninterface, vlaninterface, vlannumber)
  element = '<comment>%s</comment>' % (vlandescription, )
  element += '<tag>%s</tag>' % (vlannumber, )
  element += "<ip><entry name='%s.1/24'/></ip>" % (vlannetwork, )
  response = fwSet(fwhost, fwkey, type, action, xpath, element)
  print "%s<br>" % (response, )

def createZone(fwhost, fwkey, vlanzoneregion, vlaninterface, vlannumber):
  #Create the zone, enable user-id, and add the sub-interface
  print "Creating the zone, enable user-id in the zone, and adding the sub-interface to the zone: "
  type = "config"
  action = "set"
  xpath = "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/zone"
  element = '<entry name="%s"><network><layer3><member>%s.%s</member></layer3></network>' % (vlanzoneregion, vlaninterface, vlannumber)
  element += '<enable-user-identification>yes</enable-user-identification></entry>'
  response = fwSet(fwhost, fwkey, type, action, xpath, element)
  print "%s<br>" % (response, )

def addRouter(fwhost, fwkey, vlaninterface, vlannumber):
  #Add the sub-interface to the default router
  print "Adding the sub-interface to the default router: "
  type = "config"
  action = "set"
  xpath = "/config/devices/entry[@name='localhost.localdomain']/network/virtual-router/entry[@name='default']/interface"
  element = "<member>%s.%s</member>" % (vlaninterface, vlannumber)
  response = fwSet(fwhost, fwkey, type, action, xpath, element)
  print "%s<br>" % (response, )

def createDhcp(fwhost, fwkey, vlaninterface, vlannumber, vlannetwork):
  #Configure DHCP
  print "Conguring DHCP: "
  type = "config"
  action = "set"
  xpath = "/config/devices/entry[@name='localhost.localdomain']/network/dhcp/interface/entry[@name='%s.%s']/server" % (vlaninterface, vlannumber)
  element = "<option><dns><primary>208.67.222.222</primary><secondary>208.67.220.220</secondary></dns>"
  element += "<lease><timeout>120</timeout></lease><gateway>%s.1</gateway><subnet-mask>255.255.255.0</subnet-mask>" % (vlannetwork, )
  element += "</option><ip-pool><member>%s.10-%s.250</member></ip-pool><mode>enabled</mode>" % (vlannetwork, vlannetwork)
  response = fwSet(fwhost, fwkey, type, action, xpath, element)
  print "%s<br>" % (response, )

def createRegion(fwhost, fwkey, vlanzoneregion, vlannetwork, latitude, longitude):
  #Add a region
  print "Adding a region: "
  type = "config"
  action = "set"
  xpath = "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/region"
  element = '<entry name="%s">' % (vlanzoneregion, )
  element += "<address><member>%s.0/24</member></address>" % (vlannetwork, )
  element += "<geo-location><latitude>%s</latitude><longitude>%s</longitude></geo-location></entry>" % (latitude, longitude)
  response = fwSet(fwhost, fwkey, type, action, xpath, element)
  print "%s<br>" % (response, )

def addSecurity(fwhost, fwkey, securityrule, vlanzoneregion):
  #Add to outbound security policy
  print "Adding the source zone to the outbound security policy: "
  type = "config"
  action = "set"
  xpath = "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/rulebase/security/rules/entry[@name='%s']/from" % (securityrule, )
  element = "<member>%s</member>" % (vlanzoneregion, )
  response = fwSet(fwhost, fwkey, type, action, xpath, element)
  print "%s<br>" % (response, )

def addNat(fwhost, fwkey, natrule, vlanzoneregion):
  #Add to outbound NAT policy
  print "Adding the source zone to the outbound NAT policy: "
  type = "config"
  action = "set"
  xpath = "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/rulebase/nat/rules/entry[@name='%s']/from" % (natrule, )
  element = "<member>%s</member>" % (vlanzoneregion, )
  response = fwSet(fwhost, fwkey, type, action, xpath, element)
  print "%s<br>" % (response, )

def fwSet(fwhost, fwkey, type, action, xpath, element):
  #This actually pushes the config change to the firewall after all of the values are set - it needs better error handling...
  values = {'type': type, 'action': action, 'xpath': xpath, 'element': element, 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  r = requests.post(palocall, data=values, verify=False)
  tree = ET.fromstring(r.text)
  response = tree.find('msg')
  return response.text

print "Content-type: text/html"
print

print """
<html>
<head>
  <title>Add a VLAN</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>
<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    Add a VLAN
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

form = cgi.FieldStorage()
vlaninterface = form.getvalue("vlaninterface")
vlannumber = form.getvalue("vlannumber")
vlanzoneregion = form.getvalue("vlanzoneregion")
vlandescription = form.getvalue("vlandescription")
vlannetwork = form.getvalue("vlannetwork")

if (vlaninterface and vlannumber and vlanzoneregion and vlandescription and vlannetwork):
  print '<div class="response">'
  createSubInterface(fwhost, fwkey, vlaninterface, vlannumber, vlannetwork, vlandescription)
  createZone(fwhost, fwkey, vlanzoneregion, vlaninterface, vlannumber)
  addRouter(fwhost, fwkey, vlaninterface, vlannumber)
  createDhcp(fwhost, fwkey, vlaninterface, vlannumber, vlannetwork)
  createRegion(fwhost, fwkey, vlanzoneregion, vlannetwork, latitude, longitude)
  addSecurity(fwhost, fwkey, securityrule, vlanzoneregion)
  addNat(fwhost, fwkey, natrule, vlanzoneregion)
  print "</div>"



else:
  print """
  <div class="form1">
    <form method="post" action="/cgi-bin/vlan.cgi">
      <label>Interface</label><br>
      <select name="vlaninterface"/>
  """
  interfaces = getInterfaces(fwhost, fwkey)
  for interface in interfaces:
    print '        <option value="%s">%s</option>' % (interface['name'], interface['name'])

  print """
      </select></br>
      <label>VLAN Number (1-4096)</label><br>
      <input type="text" name="vlannumber"/><br>
      <label>Zone/Region Name</label><br>
      <input type="text" name="vlanzoneregion"/><br>
      <label>Description</label><br>
      <input type="text" name="vlandescription"/><br>
      <label>Network (10.19.xxx)</label><br>
      <input type="text" name="vlannetwork"/><br>
      <input type="submit" value="Submit"/>
    </form>
  </div>
  """

print """
  </body>
  </html>
"""
