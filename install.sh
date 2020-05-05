#!/bin/bash

#Tell the installer the root of the files to download
REPO="https://raw.githubusercontent.com/bartoqid/PAN-AF/master/"

#check to make sure Python is installed
python --version

sudo apt-get update
#install the python requests module
sudo apt-get install python-requests -y

#install sqlite3
sudo apt-get install sqlite3 -y

#install python-pip
sudo apt-get install python-pip -y

#install xmldiff
sudo apt-get install python-lxml -y
sudo pip install xmldiff

#create the directory for the primary dug code to live
cd /var
sudo mkdir dug
sudo chown www-data dug
sudo chgrp www-data dug
cd /var/dug
#create the devices database
sudo touch create.sql
sudo chmod 777 create.sql
sudo echo 'CREATE TABLE DevicesDynamic (DeviceName "TEXT", DeviceMac "TEXT", Groups "Text");' > create.sql
sudo sqlite3 devices.sql < create.sql
sudo rm create.sql
#install the code that updates the firewall
sudo wget -q ${REPO}dug.py
#create the log file
sudo touch dug.log
#Set owner, group, and permissions of files in /var/dug
sudo chown www-data *.*
sudo chgrp www-data *.*
sudo chmod 755 *.*

#update cron to execute the script every minute
cd /etc/cron.d
sudo wget -q ${REPO}dugcron

#install apache2 and configure it to allow cgi
sudo apt-get install apache2 -y
sudo a2enmod cgid
sudo service apache2 restart

#copy cgi scripts into the cgi directory
cd /usr/lib/cgi-bin
sudo wget -q ${REPO}index.cgi
sudo wget -q ${REPO}keygen.cgi
sudo wget -q ${REPO}bpatoken.cgi
sudo wget -q ${REPO}bpa.cgi
sudo wget -q ${REPO}downloadbpa.cgi
sudo wget -q ${REPO}vlan.cgi
sudo wget -q ${REPO}usermap.cgi
sudo wget -q ${REPO}groupmap.cgi
sudo wget -q ${REPO}clearusers.cgi
sudo wget -q ${REPO}arp.cgi
sudo wget -q ${REPO}dhcp.cgi
sudo wget -q ${REPO}dhcputil.cgi
sudo wget -q ${REPO}policy.cgi
sudo wget -q ${REPO}duglog.cgi
sudo wget -q ${REPO}syslog.cgi
sudo wget -q ${REPO}messageslog.cgi
sudo wget -q ${REPO}accesslog.cgi
sudo wget -q ${REPO}errorlog.cgi
sudo wget -q ${REPO}manback.cgi
sudo wget -q ${REPO}software.cgi
sudo wget -q ${REPO}changes.cgi
sudo wget -q ${REPO}menu.html
sudo chown www-data *.*
sudo chgrp www-data *.*
sudo chmod 755 *.*

cd /etc/rsyslog.d
sudo rm -f 50-default.conf
sudo wget -q ${REPO}50-default.conf
sudo service rsyslog restart
#log permissions and rotation configuration
sudo chmod 644 /var/log/syslog
sudo chmod 644 /var/log/messages
cd /etc
sudo rm rsyslog.conf
sudo wget -q ${REPO}rsyslog.conf
sudo chown root rsyslog.conf
sudo chgrp root rsyslog.conf
sudo chmod 755 rsyslog.conf
sudo rm logrotate.conf
sudo wget -q ${REPO}logrotate.conf
sudo chown root logrotate.conf
sudo chgrp root logrotate.conf
sudo chmod 755 logrotate.conf

sudo chmod 755 /var/log/apache2
sudo chmod 644 /var/log/apache2/access.log
sudo chmod 644 /var/log/apache2/error.log
cd /etc/logrotate.d
sudo rm apache2
sudo wget -q ${REPO}apache2
sudo chown root apache2
sudo chgrp root apache2
sudo chmod 644 apache2

#copy default web pages
cd /var/www/html
sudo rm index.html
sudo wget -q ${REPO}index.html
sudo wget -q ${REPO}logo.png
sudo wget -q ${REPO}style.css
sudo wget -q ${REPO}favicon.ico
sudo touch macs.txt
sudo touch rsa.csv
sudo chown www-data *.*
sudo chgrp www-data *.*
sudo chmod 755 *.*

cd /var
sudo mkdir autoback
sudo chown www-data autoback
sudo chgrp www-data autoback
cd /var/autoback
sudo wget -q ${REPO}autoback.py
sudo chown www-data *.*
sudo chgrp www-data *.*
sudo chmod 755 *.*

#harden the Raspberry Pi
#sudo systemctl disable avahi-daemon
#sudo systemctl stop avahi-daemon
#sudo systemctl disable triggerhappy
#sudo systemctl stop triggerhappy

#harden Apache
#cd /etc/apache2/conf-available
#sudo rm -y security.conf
#sudo wget -q ${REPO}security.conf
#sudo systemctl restart apache2
