Sniffo

A 802.11 Probe Request Sniffer developed over Scapy (Python). This sniffer attempts to capture all the Probe Requests touching a Wireless interface (in monitor mode) and extracts the MAC, Signal Strength. Values extracted are pushed into a MySQL Database.

** Prerequisities **
 - Python 2.7 (This has been tested on Python 2.7, though it might as well work with Python 3)
 - Scapy (Compatible with Python 2.7)
 ** For Installing Scapy, use standard package managers of DEB or RPM builds
 **  For Debian:     $ sudo apt-get install python-scapy
 **  For Fedora/RPM: $ sudo yum install python-scapy
 **  Python PIP may also work
 - MySQL (v5.6)
 **  For Debian:     $ sudo apt-get install mysql-server mysql-common
 **  For Fedora/RPM: $ sudo yum install mysql-server mysql-common
 - Before the Script is executed, the Database and the table in it should be configured
 ** Name of the Database, its table, credentials should be modified in the script
 ** Look for global identifiers DB_NAME, DB_TABLE, DB_USERNAME and DB_PASSWORD
 ** If a network/remote DB is used, update the DB_HOST field as well
 ** For creating the table, refer the wifiscan.sql file in this repository. It contains the Schema

** Execution **
 - The script takes as input the name of the interface which has been configured in Monitor mode. 
 ** If the interface is not in monitor mode, the script would fail to work
 - Execution sample:
 ** $ sudo python wifiscan.py wlan0
 ** in which, 'sudo' is for providing privileges to use packet capturing, and 'wlan0' is name of interface
