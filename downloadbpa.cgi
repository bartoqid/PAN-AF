#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(format='text')  # for troubleshooting
import sys
import time
import urllib
import requests
import datetime
import json 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET
sys.path.insert(0, '/var/dug/')

import fw_creds
fwhost = fw_creds.fwhost
fwkey = fw_creds.fwkey
import bpatokenfile
token = bpatokenfile.bpatoken

currenttime = '{:%d-%m-%Y-%H%M%S}'.format(datetime.datetime.now())

def get_system_info(firewall_ip, api_key):
    values = {'type': 'op', 'cmd': '<show><system><info></info></system></show>', 'key': api_key}
    call = 'https://%s/api/' % (firewall_ip)

    response = requests.post(call, data=values, verify=False)

    tree = ET.fromstring(response.text)

    if tree.get("status") == "success":
        return tree

    else:
        return false

def get_license(firewall_ip, api_key):
    values = {'type': 'op', 'cmd': '<request><license><info></info></license></request>', 'key': api_key}
    call = 'https://%s/api/' % (firewall_ip)

    response = requests.post(call, data=values, verify=False)

    tree = ET.fromstring(response.text)

    if tree.get("status") == "success":
        return tree
        print tree
    else:
        return false

def get_running_config(firewall_ip, api_key):
    values = {'type': 'config', 'action': 'show', 'key': api_key}
    call = 'https://%s/api/' % (firewall_ip)

    response = requests.post(call, data=values, verify=False)

    tree = ET.fromstring(response.text)

    if tree.get("status") == "success":
        return tree
    else:
        return false

def get_time(firewall_ip, api_key):
    values = {'type': 'op', 'cmd': '<show><clock></clock></show>', 'key': api_key}
    call = 'https://%s/api/' % (firewall_ip)

    response = requests.post(call, data=values, verify=False)

    tree = ET.fromstring(response.text)

    if tree.get("status") == "success":
        return tree
        print tree
    else:
        return false

def get_result(task_id, token):
    auth = {'Authorization': 'Token %s' % token}
    call = 'https://bpa.paloaltonetworks.com/api/v1/results/' + task_id
    response = requests.get(call, headers=auth, verify=False)
    status = json.loads(response.content)
    
    while "processing" in status["status"]:
	time.sleep(3)
	auth = {'Authorization': 'Token %s' % token}
        call = 'https://bpa.paloaltonetworks.com/api/v1/results/' + task_id
        response = requests.get(call, headers=auth, verify=False)
        status = json.loads(response.content)


def submit_bpa(xml, info, license, gettime, token):
    values = {'xml': xml, 'system_info': info,  'license_info': license, 'system_time': gettime, 'generate_zip_bundle': 'true'}
    auth = {'Authorization': 'Token %s' % token}
    call = 'https://bpa.paloaltonetworks.com/api/v1/create/'
    response = requests.post(call, headers=auth, data=values, verify=False)
    taskid = json.loads(((response.text).encode('utf-8')))
    resultid = taskid["task_id"]
    return resultid

def download_bpa(task_id, token, firewall_ip):
    auth = {'Authorization': 'Token %s' % token}
    call = 'https://bpa.paloaltonetworks.com/api/v1/results/' + task_id + '/download/'

    print 'Content-Type: application/zip'
    print 'Content-Disposition: attachment; filename="%s-%s.zip"\n' % (firewall_ip, currenttime)
    response = requests.get(call, headers=auth, verify=False, stream=True)
    print(response.content)


treesystem = get_system_info(fwhost, fwkey)
systeminfo = ET.tostring(treesystem)

treerun = get_running_config(fwhost, fwkey)
runconfig = ET.tostring(treerun)

treelicense = get_license(fwhost, fwkey)
licenseinfo = ET.tostring(treelicense)

treetime = get_time(fwhost, fwkey)
showtime = ET.tostring(treetime)

bpataskid = submit_bpa(runconfig, systeminfo, licenseinfo, showtime, token)
	
get_result(bpataskid, token)

download_bpa(bpataskid, token, fwhost)
