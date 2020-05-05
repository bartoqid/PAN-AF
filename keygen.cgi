#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(format='text')  # for troubleshooting
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET

fwcredsfile = "/var/dug/fw_creds.py"

print "Content-type: text/html"
print

print """
<html>
<head>
  <title>Generate Key</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>
<body>
<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    Generate Key
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

form = cgi.FieldStorage()
fwip = form.getvalue("fwip")
fwusername = form.getvalue("fwusername")
fwpassword = form.getvalue("fwpassword")

if (fwip and fwusername and fwpassword):
  values = {'type': 'keygen', 'user': fwusername, 'password': fwpassword}
  apicall = 'https://%s/api/' % (fwip, )
  response = requests.post(apicall, data=values, verify=False)
  if response:
    tree = ET.fromstring(response.text)
    if tree.get('status') == "success":
      fwkey = tree.find('./result/key').text
  if fwkey:
    file = open(fwcredsfile, "w")
    line = 'fwhost = "%s"\n' % (fwip, )
    file.write(line)
    line = 'fwkey = "%s"\n' % (fwkey, )
    file.write(line)
    file.close()

    print '<div class="response">'
    print "IP: %s<br>\n" % (fwip, )
    print "Key: %s<br>\n" % (fwkey, )
    print "<br>\n"
    print "Successfully written to the credential store."

else:
  print """
<div class="form1">
  <form method="post" action="/cgi-bin/keygen.cgi">
    <label>Firewall IP Address or Hostname</label><br>
    <input type="text" name="fwip"/><br>
    <label>User</label><br>
    <input type="text" name="fwusername"/><br>
    <label>Password</label><br>
    <input type="password" name="fwpassword"/><br>
    <input
     type="submit" value="Submit"/>
  </form>
</div>
</body>
</html>
  """
