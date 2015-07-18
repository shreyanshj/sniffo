Sniffo

A 802.11 Probe Request Sniffer developed over Scapy (Python). This sniffer attempts to capture all the Probe Requests touching a Wireless interface (in monitor mode) and extracts the MAC, Signal Strength. Values extracted are pushed into a MySQL Database.

** Prerequisities **
 1) Python 2.7 (This has been tested on Python 2.7, though it might as well work with Python 3)

 2) Scapy (Compatible with Python 2.7)
 ** For Installing Scapy, use standard package managers of DEB or RPM builds
 **  For Debian:     $ sudo apt-get install python-scapy
 **  For Fedora/RPM: $ sudo yum install python-scapy
 **  Python PIP may also work
 ** Refer http://www.secdev.org/projects/scapy/doc/installation.html for more details
 
 3) MySQL (v5.6)
 **  For Debian:     $ sudo apt-get install mysql-server mysql-common
 **  For Fedora/RPM: $ sudo yum install mysql-server mysql-common
 ** Refer http://dev.mysql.com/doc/refman/5.6/en/installing.html for more details


** Installation and Execution **

 1) Before the software is executed, the MySQL Database and the table in it should be pre-configured
 ** Refer file wifiscan.sql for the DB SCHEMA
 ** Use the following command line snippet as hint for creating the databse named 'wifiscan' and table named 'client'
 ---8<----
 # $ mysql -u <username> -p
 # [after logging into mysql]
 # mysql> CREATE DATABASE wifiscan;
 # mysql> USE wifiscan
 # mysql> CREATE TABLE client {
 #         `id` int(6) NOT NULL AUTO_INCREMENT,
 #         `timestamp` int(11) DEFAULT NULL,
 #         `mac` varchar(17) DEFAULT NULL,
 #         `rssi` tinyint(3) DEFAULT NULL,
 #         `location` varchar(20) DEFAULT NULL,
 #         PRIMARY KEY (`id`)
 #         ) ENGINE=InnoDB AUTO_INCREMENT=159 DEFAULT CHARSET=latin1;
 # mysql> DESCRIBE client;
    
 2) If you choose to use different names for Database and Table
 ** Name of the Database, its table, credentials should be modified in the script 'wifiscan.py'
 ** Look for global identifiers DB_NAME, DB_TABLE, DB_USERNAME and DB_PASSWORD
 ** If a network/remote DB is used, update the DB_HOST field as well

** Execution **

 1) Once the database is created, use the following command to execute the software:
 $ sudo python wifiscan.py wlan0
 where 'wlan0' is assumed to be name of the Wireless interface on which probing is required

 2) Execution sample:
 ** $ sudo python wifiscan.py wlan0
 ** in which, 'sudo' is for providing privileges to use packet capturing, and 'wlan0' is name of interface

** Synchronization of DB across Hosts **

 For synchronization of DB across a network, we can use combination of mysql dump + rsync + crond
 mysql Dump: Mysql supports dumping of DB in a raw format which can be used for restoring at another location
        $ mysqldump --databases wifiscan > wifiscan-dumped.sql
        would dump the current state of Database into 'wifiscan-dumped.sql' file.
        This file can then be candidate for synching through rsync

 rsync: Is a tool for moving files across network, from one host to another.
        rsync handles differences in file to reduce network traffic by only moving modified part
        Example Command:
        $ rsync -az <name of local file> <username@remote_host:name of destination file or blank>
        for example, using the wifiscan-dump.sql file:
        $ rsync -az wifiscan-dump.sql remoteuser@remotemachine:/path/to/synchronized_dump_file
        It is important to note that SSH keys might have to pre-shared if no-prompt rsync is expected

 crond: Is a Linux System Scheduler for tasks
        Please note that for coupling rsync with crond, SSH Key sharing would be required else the sync would fail
        For crond, use a line like the following in the /etc/cron.d/<> file
        <min> <hour> <day of month> <month> <day of week> <command: rsync -az local-file remote-file>

        Thus, for synchronizing once for each hour:
        * 2 * * * rsync -az wifiscan-dump.sql <remote location>

Restoring the Dump file:
        On the remote machine, one can perform MySQL restore
        $ mysql -u <mysql user> -p wifiscan < wifiscan-dump.sql
        Would restore the database into the remote machine's MySQL Engine.
