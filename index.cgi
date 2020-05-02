#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(format='text')  # for troubleshooting
import sqlite3

dbfile = "/var/dug/devices.sql"

print "Content-type: text/html"
print

print """
<html>
<head>
  <title>Manage Dynamic Devices</title>
  <link rel="stylesheet" href="/style.css" type="text/css">
</head>

<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.png" height="75px">
  </div>
  <div class="text">
    Dynamic User System
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

form = cgi.FieldStorage()
devicename = form.getvalue("devicename")
devicemac = form.getvalue("devicemac")
devicetag = form.getvalue("devicetag")
devicedelete = form.getvalue("devicedelete")

if (devicedelete):
  print devicedelete
  conn = sqlite3.connect(dbfile)
  cursor = conn.cursor()
  try:
    cursor.execute('DELETE FROM DevicesDynamic WHERE DeviceName = ?', (devicedelete, ))
  except sqlite3.Error as e:
    print e.args[0]
  conn.commit()
  conn.close()

if (devicename and devicemac):
  conn = sqlite3.connect(dbfile)
  cursor = conn.cursor()
  values = (devicename, devicemac, devicetag)
  cursor.execute('INSERT INTO DevicesDynamic ("DeviceName", "DeviceMac", "Groups") VALUES (?,?,?)', values)
  conn.commit()
  conn.close()

print """
<div class="form1">
  <form method="post" action="/cgi-bin/index.cgi">
    <label>Name</label><br>
    <input type="text" name="devicename"/><br>
    <label>MAC Address</label><br>
    <input type="text" name="devicemac"/><br>
    <label>Group</label><br>
    <input type="text" name="devicetag"/><br>
    <input type="submit" value="Submit"/>
  </form>
</div>
"""

conn = sqlite3.connect(dbfile)
cursor = conn.cursor()
cursor.execute('select DeviceName, DeviceMac, Groups from DevicesDynamic order by Groups')
rows = cursor.fetchall()

print """
<div class="form2">
  <form method="post" action="/cgi-bin/index.cgi">
    <table>
      <col class="radiocolumn" />
      <col class="datacolumn" />
      <col class="datacolumn" />
      <col class="datacolumn" />
      <tr>
        <th>Delete</th>
        <th>Device Name</th>
        <th>MAC Address</th>
        <th>Group</th>
      </tr>
"""

for row in rows:
  print '      <tr><td align="center"><input type="radio" name="devicedelete" value="%s"/></td>' % (row[0], )
  for field in row:
    print "       <td>%s</td>" % (field, )
  print "      </tr>"

conn.close()

print """
    </table>
    <input type="submit" value="Submit">
  </form>
</div>
</body>
</html>
"""
