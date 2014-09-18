#!/bin/sh

cd /usr/share/doc/ndoutils-mysql-1.5.2/db
mysql -uroot ndoutils < mysql.sql
