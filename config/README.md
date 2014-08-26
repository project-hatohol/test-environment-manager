#test-environment-manager /config

##Summary

This tools configure hatohol test environment.

##Configuration tool execution environment

This tool will work in the following environments.

* HostOS:Ubuntu
* LXC (Linux Containers)
* Ruby 2.0
* Rake
* bundler
* ruby-lxc

##Support Middleware

This tools can setting the following software:

* GuestOS:centos 6.5 x64
* zabbix server mysql ver 2.2.5,2.0.12
* zabbix agent ver 2.2.5,2.0.12
* nagios (includes ndoutils ver 1.5.2)  ver 3.5.1
* redmine ver 2.4.6
 - Ruby 2.0.0-p481
 - passenger ver 4.0.49

##Installation

Install some packages.

	$ sudo apt-get install lxc lxctl lxc-dev ruby2.0 ruby2.0-dev

>*Note:*
>*Run update-alternatives command to update aliases as necessary.*

Clone source from Github

	$ git clone https://github.com/project-hatohol/test-environment-manager.git


Run bundle install

	$ cd test-environment-manager/config
	$ sudo bundle install


##Container construction

###Step1 Create a virtual machine

Install on the host computer some program of required to set up the virtual machine.

	$ sudo apt-get -y install lxc yum rpm


Create a virtual machine on the host computer.

	$ sudo lxc-create -t centos -n ${Container_Name}


When initialization is complete, run the following command for setting password:

	$ sudo chroot /var/lib/lxc/temp/rootfs passwd


Next, login the virtual machine:

	$ sudo lxc-start -n ${Container_Name} -d
	$ sudo lxc-console -n ${Container_Name}

You should use username as ‘root’.

###Step2 Install Basic Softwares

The following all tasks run on the console of the virtual machine.

1. Install Apache

 Run those commands:

		# yum -y install httpd httpd-devel
		# service httpd start
		# chkconfig httpd on

2. Install MySQL

 Run the following command:

		# yum -y install mysql mysql-server mysql-devel


 Edit the following files in any editor:

		# ${any_editor} /etc/my.cnf


 Add the following into the key of [mysqld] :

		character-set-server = utf8


 Run the following command for start the MySQL:

		# /etc/rc.d/init.d/mysqld start
		# chkconfig mysqld on


 Run the following command for first setting for MySQL:

		# mysql_secure_installation


###Step3 Install Middlewares

*Install middlewares which needed.*
*These are example for recommended middlewares. You don’t have to do all tasks.*

* Install Zabbix-Server

 Add repository and Install packages

		# rpm -ivh http://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm
		# yum update
		# yum install zabbix-server-mysql zabbix-web-mysql


 Create database on MySQL for Zabbix-Server

		# mysql -u root -p
		> create database ${zabbix_DBName} character set utf8;
		> grant all privileges on ${zabbix_DBName}.* to ${zabbix_DBUser}@localhost identified by '${zabbix_DBPassword}';
		> exit
		# cd /usr/share/doc/zabbix-server-mysql-2.2.5/create
		# mysql -u root -p zabbix < schema.sql
		# mysql -u root -p zabbix < images.sql
		# mysql -u root -p zabbix < data.sql


* Install Zabbix-Agent
 Add repository and Install packages

		# rpm -ivh http://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm
		# yum update
		# yum install zabbix-agent


* Install Nagios(ndoutils)
 Add repository and Install packages

		# rpm -Uvh http://ftp.jaist.ac.jp/pub/Linux/Fedora/epel/6/i386/epel-release-6-8.noarch.rpm
		# yum update
		# yum install nagios nagios-common nagios-plugins-all ndoutils ndoutils-mysql


 Create database on MySQL for Nagios
 

		# mysql -u root
		> create database \${database_name};
		> grant all on ${database_name}.* to ${database_username}@'%' identified by '${database_password}';
		> flush privileges;
		> exit
		# cd /usr/share/doc/ndoutils-mysql-1.5.2/db
		# mysql -D ndoutils < mysql.sql

* Install Redmine

 Install Ruby

		# yum groupinstall "Development tools"
		# yum install zlib-devel sqlite sqlite-devel wget openssl-devel readline-devel curl-devel libyaml-devel mysql-devel
		# curl -O http://cache.ruby-lang.org/pub/ruby/2.0/ruby-2.0.0-p481.tar.gz
		# tar xvf ruby-2.0.0-p481.tar.gz
		# cd ruby-2.0.0-p481
		# make
		# make install
		# gem install bundler

 Install Redmine

		# curl -O http://www.redmine.org/releases/redmine-2.4.6.tar.gz
		# tar xvf redmine-2.4.6.tar.gz
		# cp -r redmine-2.4.6 /var/lib/redmine


 Create database on MySQL for Redmine

		# mysql -u root -p
		> create database ${database_name} default character set utf8;
		> grant all on ${database_name}.* to '${database_username}'@'localhost' identified by '${database_password}';


 Set document root path to redmine

		# ${any_editor} /etc/httpd/conf/httpd.conf
		DocumentRoot "/var/lib/redmine/public"
		
 Install apache plugin for ruby

		# gem install passenger
		# passenger-install-apache2-module
		# passenger-install-apache2-module --snippet >> /etc/httpd/conf.d/passenger.conf

##Configuration File

Settings into “test-environment-manager/config/config/container.yml”

```
<example>
sample-container: #container name
  container_path: /var/lib/lxc/sample-container #container save location
  ipaddress: 10.0.3.10 #ip address
  base_container: sample-container-base #clone container source
  zabbix-server: #Settigs for zabbix server
    database_name: zabbix
    database_username: zabbix
    database_password: admin
  zabbix-agent: #Settings for zabbix agent
    server_ipaddress: 10.0.3.10
    host_name: “Zabbix Server”
```

Write all settings with hash.
Top Level Object is container name to configure.

Setting Description

* container_path - container save location: There are rootfs directory and config file.
* ipaddress - Static IP Address for container
base_container - clone container source
* zabbix-server - Settings for Zabbix Server
 - database_name - Database name for Zabbix Server
 - database_username - Database user name for Zabbix Server
 - database_password - Database password for Zabbix Server
* zabbix-agent - Settings for Zabbix Agent
 - server_ipaddress - Monitoring data destination address
 - host_name - Identifier of this container
* nagios - Settings for Nagios
 - database_name - Database name for Nagios
 - database_username - Database user name for Nagios
- database_password - Database password for Nagios
* redmine - Settings for Redmine
 - database_name - Database name for Redmine
 - database_username - Database user name for Redmine
 - database_password - Database Password for Redmine

List of Settings position

|Setting Key|Position|
|:---|:---|
|container_path|\-|
|ipaddress|\${container_path}/config <br> - lxc.network.ipv4 = \${ipaddress} <br> \${container_path}/rootfs/etc/network-scripts/ifcfg-etho <br> - BOOTPROTO = static|
|base_container|-|
|zabbix-server|\${container_path}/rootfs/etc/httpd/conf.d/zabbix.conf <br> - php_value date.timezone Asia/Tokyo|
|-database_name<br>-database_username <br> - database_password|\${container_path}/rootfs/etc/zabbix/zabbix_server.conf <br> - DBName=\${database_name} <br> - DBUser=\${database_username} <br> - DBPassword=\${database_password}|
|zabbix-agent|-|
|-server_ipaddress<br>-host_name|\${container_path}/rootfs/etc/zabbix/zabbix_agentd.conf <br> - Server=\${server_ipaddress} <br> - Hostname=\${host_name}|
|nagios|\${container_path}/rootfs/etc/nagios/nagios.cfg <br> -broker_module=usr/lib64/nagios/brokers/ndomod.so config_file=/etc/nagios/ndomod.cfg|
|-database_name<br>-database_username<br>-database_password|\${container_path}/rootfs/etc/nagios/ndo2db.cfg <br> - db_name=\${database_name} <br> - db_user=\${database_username} <br> - db_password=\${database_password}|
|redmine|-|
|-database_name<br>-database_username<br>-database_password|\${container_path}/rootfs/var/lib/redmine/config/database.yml <br> - production <br> - database: \${database_name} <br> - username: \${database_username} <br> - password: \${database_password}|


##Tasks

* rake config
 - Configure all containers
* rake status
 - Show status and ip address of all containers
* rake start
 - Start all containers
* rake shutdown
 - Shutdown all containers
* rake showip
 - Show ip address of all containers
* rake reboot
 - Reboot all containers
* rake build
 - Clone all containers as base_container
* rake destroy
 - Destroy all containers
* rake rebuild
 - Call destroy task and build task

##Usage

Write settings to test-environment-manager/config/config/containers.yml
Change working directory.

	$ cd test-environment-manager/configs

If you want clone containers, you should run this command.

	$ sudo bundle exec rake build

Run Configuration

	$ sudo bundle exec rake config

When configuration finished, shutdown all containers.

	$ sudo bundle exec rake shutdown

Start up again

	$ sudo bundle exec rake start

Warning）Don’t run “bundle exec rake reboot”. LXC assign Incorrect IP address to containers.
Run the following command for check correct IP addresses has been set:

	$ sudo bundle exec rake status

Log in to each container, to start the services.
