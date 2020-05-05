Thanks to Dan Ward who put together this framework
I will try to maintain this, make sure it is compatible with different version of PAN-OS
and more importantly add more features.

This lates code has been tested using Ubuntu 16.04 and 18.04 with PAN-OS 8.1, 9.0 and 9.1
Any issue/bug, let me know and I will get it fixed

### New Feature May 2020
####BPA Automation
This feature requires BPA token and will automate the submission and creation of BPA reports and download the reports as zip file.


# PAN-AF

This project is an automation framework for Palo Alto Networks firewalls.  Instead of creating the same components for each new project (credential generation/storage, web framework, etc...), I opted to put my automation efforts into this framework.

### Dynamic User Groups for Palo Alto Networks devices

This package does quite a lot around dynamic user and dynamic group registration.  The idea is to give you something consistent to correlate activity around as IP addresses change in a dynamic network.  If you know more information about the device, you may add it in the database using the web interface.  Otherwise, the code generates a user-id based on mac info and hostname if it is provided when requesting a DHCP lease.

The logic is as follows:
1. Collect all DHCP leases from the firewall
2. Collect all ARP entries from the firewall (This captures devices with static IP addresses)
3. Poll all MAC addresses in the database
4. If the MAC is in the database, assign the name and group from the database
5. If the MAC is not in the database and the hostname is available, assign a name based on MAC plus hostname
6. If the MAC is not in the database and the hostname is not available, assign a name based on the MAC address only
7. Upload all of the device-name-to-user-id-mappings and user-id-to-group-mappings to the firewall

### To install this branch, issue the following commands:
```
wget -q https://raw.githubusercontent.com/p0lr/PAN-AF/master/install.sh
chmod +x install.sh
./install.sh
```

### To use:
```
Browse to http://<ip>
Click on the Palo Alto Networks logo
Click on "Manage Firewall" in the navigation menu
Enter the firewall IP address or hostname, username, and password for an account that has the proper permissions
Click on "Generate Key" in the navigation menu
Add your devices
```

### That's it!
- The firewall logs will now show your IP addresses with the appropriate names.
- If you registered any devices in groups, the group names will automatically appear in source and destination drop-downs in the firewall management interface.

### BONUS
So much automation!
