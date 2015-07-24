#!/bin/bash
. ./wifiscan.conf

mysqladmin -u $DB_USERNAME -p$DB_PASSWORD  create $DB_NAME
mysql -u $DB_USERNAME -p$DB_PASSWORD $DB_NAME < ./wifiscan.sql
cp -f sniffstart /etc/init.d/
cp -f wifiscan.conf /etc/
cp -f wifiscan.py $INSTALL_DIR/
cp -f sniffcron $INSTALL_DIR/
update-rc.d sniffstart defaults
mkdir -p $DB_LOCAL
crontab -l > /tmp/cronlist
echo "0 * * * * sh $INSTALL_DIR/sniffcron" >> /tmp/cronlist
crontab /tmp/cronlist
rm -f /tmp/cronlist

