#!/bin/sh

cd /usr/share/doc/zabbix-server-mysql-2.0.12/create/
mysql -uroot zabbix < schema.sql
mysql -uroot zabbix < images.sql
mysql -uroot zabbix < data.sql

