#!/usr/bin/env python
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET
import fw_creds
import sqlite3
import StringIO
import datetime

fwhost = fw_creds.fwhost
fwkey = fw_creds.fwkey
dbfile = "/var/dug/devices.sql"
rsafile = "/var/www/html/rsa.csv"
macfile = "/var/www/html/macs.txt"

def getDhcp(fwhost, fwkey):

  values = {'type': 'op', 'cmd': '<show><dhcp><server><lease><interface>all</interface></lease></server></dhcp></show>', 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  r = requests.post(palocall, data=values, verify=False)
  leases = []
  dhcptree = ET.fromstring(r.text)
  for lease in dhcptree.findall('./result/interface/entry'):
    info = {}
    if (lease.find('state').text == "committed"):
      info['ip'] = lease.find('ip').text
      info['mac'] = lease.find('mac').text
      if lease.find('hostname') is not None:
        info['host'] = lease.find('hostname').text
        info['sysname'] = "%s-%s" % (lease.find('mac').text, lease.find('hostname').text)
      else:
        info['sysname'] = lease.find('mac').text
      leases.append(info)
  return leases

def getArp(fwhost, fwkey):
  output = []
  values = {'type': 'op', 'cmd': '<show><arp><entry name ="all"/></arp></show>', 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  r = requests.post(palocall, data=values, verify=False)
  arptree = ET.fromstring(r.text)
  for entries in arptree.findall('./result/entries'):
    for entry in entries.findall('entry'):
      if entry.find('mac').text <> "(incomplete)":
        info = {}
        info['ip'] = entry.find('ip').text
        info['mac'] = entry.find('mac').text
        info['sysname'] = entry.find('mac').text
        output.append(info)
  return output

def getDatabase(dbfile):
  conn = sqlite3.connect(dbfile)
  cursor = conn.cursor()
  cursor.execute('select DeviceName, DeviceMac, Groups from DevicesDynamic')
  responses = cursor.fetchall()

  output = []
  for response in responses:
    output.append( {"mac": response[1], "name": response[0], "group": response[2]} )

  return output

def enrichArp(leases):
  arps = getArp(fwhost, fwkey)
  for arp in arps:
    addarp = True
    for lease in leases:
      if arp['mac'] == lease['mac']:
        addarp = False

    if addarp:
      leases.append(arp)

  return leases

def enrichDatabase(leases):
  databases = getDatabase(dbfile)
  output = []
  for lease in leases:
    for record in databases:
      if (lease['mac'] == record['mac']):
        lease['sysname'] = record['name']
        lease['group'] = record['group']
    output.append(lease)
  return output

def fwFormat(hostdata):
  fwxml = '<uid-message>\n'
  fwxml += '\t<version>1.0</version>\n'
  fwxml += '\t<type>update</type>\n'
  fwxml += '\t<payload>\n'
  fwxml += '\t\t<login>\n'
  for entry in hostdata:
    fwxml += '\t\t\t<entry name="%s" ip="%s" timeout="30"/>\n' % (entry['sysname'], entry['ip'])
  fwxml += '\t\t</login>\n'
  fwxml = fwxml + '\t\t<groups>\n'
  groups = []
  for entry in hostdata:
    if entry.has_key('group'):
      if entry['group'] not in groups:
        groups.append(entry['group'])
  for group in groups:
    fwxml += '\t\t\t<entry name="%s">\n' % (group, )
    fwxml += '\t\t\t\t<members>\n'
    for entry in hostdata:
      if entry.has_key('group'):
        if (entry['group'] == group):
          fwxml += '\t\t\t\t\t<entry name="%s"/>\n' % (entry['sysname'], )
    fwxml += '\t\t\t\t</members>\n'
    fwxml += '\t\t\t</entry>\n'
  fwxml += '\t\t</groups>\n'
  fwxml += '\t</payload>\n'
  fwxml += '</uid-message>'
  return fwxml

def rsaWrite(hostdata):
  rsacsv = 'mac,ip,sysname,host,group\n'
  for entry in hostdata:
    rsacsv += "%s,%s,%s" % (entry['mac'], entry['ip'], entry['sysname'])
    if entry.has_key('host'):
      rsacsv += ',%s' % (entry['host'], )
    else:
      rsacsv += ','
    if entry.has_key('group'):
      rsacsv += ',%s' % (entry['group'], )
    else:
      rsacsv += ','
    rsacsv += '\n'
  file = open(rsafile,"w+")
  file.write(rsacsv)
  file.close

def macWrite(hostdata):
  file = open(macfile, "r+")
  readmacs = file.read().split("\n")

  fwmacs = []
  for entry in hostdata:
    fwmacs.append(entry['mac'])

  for mac in fwmacs:
    if mac not in readmacs:
      file.write("%s\n" % (mac, ))

def fwWrite(fwxml):
  values = {'type': 'user-id', 'key': fwkey, 'cmd': fwxml}
  palocall = 'https://' + fwhost + '/api'
  r = requests.post(palocall, data=values, verify=False)
  rtree = ET.fromstring(r.text)
  return rtree.get('status')


#Get DHCP Leases from the firewall
leases = getDhcp(fwhost, fwkey)

#Add statically-assigned IP address data from the ARP table
arps = enrichArp(leases)

#Enrich the entries with data from the DUG database
hostdata = enrichDatabase(arps)

#Write out the csv data for RSA ingestion
rsaWrite(hostdata)

#Write new unique mac addresses to the mac list
macWrite(hostdata)

#Format the data into an XML update for the firewall
fwxml = fwFormat(hostdata)

#Write the data to the firewall
stat = fwWrite(fwxml)

log = open("/var/dug/dug.log", "a")
log.write(str(datetime.datetime.now()) + ": " + stat + "\n")
log.close
