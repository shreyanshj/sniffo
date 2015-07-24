#!/bin/bash
. /etc/wifiscan.conf

mysqladmin -f -u$DB_USERNAME -p$DB_PASSWORD drop $DB_NAME
update-rc.d -f sniffstart remove 
rm -f $INSTALL_DIR/wifiscan.py
rm -f $INSTALL_DIR/sniffcron
rm -f /etc/wifiscan.conf
rm -f /etc/init.d/sniffstart
