#!/bin/sh

NAGIOS_NAME=nagios-4.0.8
PLUGIN_NAME=nagios-plugins-2.0
NDOUTILS_NAME=ndoutils-2.0.0
NRPE_NAME=nrpe-2.15
NAGIOS_ETC_PATH=/usr/local/nagios/etc

cd $NAGIOS_NAME
./configure --with-command-group=nagios
make all
make fullinstall
make install-config

cp -R contrib/eventhandlers/ /usr/local/nagios/libexec/
chown -R nagios:nagios /usr/local/nagios/libexec/eventhandlers

/usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg
/etc/init.d/nagios start

/etc/init.d/httpd start

cd ../$PLUGIN_NAME
./configure --with-nagios-user=nagios --with-nagios-group=nagios
make
make install

cd ../$NDOUTILS_NAME
./configure
make
make fullinstall
cp src/ndo2db-4x src/ndomod-4x.o /usr/local/nagios/bin
mv $NAGIOS_ETC_PATH/ndo2db.cfg-sample $NAGIOS_ETC_PATH/ndo2db.cfg
mv $NAGIOS_ETC_PATH/ndomod.cfg-sample $NAGIOS_ETC_PATH/ndomod.cfg
mysql -uroot ndoutils < db/mysql.sql

cd ../$NRPE_NAME
./configure
make all
make install-plugin

chkconfig --add nagios
chkconfig nagios on
chkconfig --add ndo2db
chkconfig ndo2db on
chkconfig httpd on
