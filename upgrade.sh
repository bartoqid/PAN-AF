#!/bin/bash

#Tell the installer the root of the files to download
REPO="https://raw.githubusercontent.com/bartoqid/PAN-AF/master/"

cd /usr/lib/cgi-bin
sudo rm menu.html
sudo wget -q ${REPO}bpatoken.cgi
sudo wget -q ${REPO}bpa.cgi
sudo wget -q ${REPO}downloadbpa.cgi
sudo wget -q ${REPO}menu.html
sudo chown www-data *.*
sudo chgrp www-data *.*
sudo chmod 755 *.*

cd /var/www/html
sudo rm index.html
sudo wget -q ${REPO}menu.html
sudo wget -q ${REPO}index.html
sudo wget -q ${REPO}logo.png
sudo chown www-data *.*
sudo chgrp www-data *.*
sudo chmod 755 *.*