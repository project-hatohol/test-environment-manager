#!/usr/bin/env python3
import lxc
import os
import sys
import definevalue
from utils import *

def create_base(container, container_name):
    container.create("centos")
    print_success_message(container_name)

    EPEL_URL = "http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
    CMDS = [["yum", "upgrade", "-y"],
            ["yum", "groupinstall", "-y", "Development Tools"],
            ["rpm", "-ivh", EPEL_URL]]

    container.start()
    container.get_ips(timeout=definedvalue.TIMEOUT_VALUE)
    print("Input password for root account:")
    container.attach_wait(lxc.attach_run_command, ["passwd"])

    for arg in CMDS:
        container.attach_wait(lxc.attach_run_command, arg)

    shutdown_container(container)


def create_zabbix_server22(contatiner_name, base):
    container = base.clone(container_name, bdevtype="aufs",
                           flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(container_name)

    RPM_URL = "http://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm"
    SCRIPT_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/import_zabbixdb22.sh"
    SCRIPT_NAME = "import_zabbixdb22.sh"
    CMDS = [["rpm", "-ivh", RPM_URL],
            ["yum", "install", "-y", "mysql-server", "httpd",
             "zabbix-server-mysql", "zabbix-web-mysql", "zabbix-agent"],
            ["service", "mysqld", "start"],
            ["chkconfig", "mysqld", "on"],
            ["yum", "install", "-y", "mysql-server", "httpd",
             "zabbix-server-mysql", "zabbix-web-mysql", "zabbix-agent"],
            ["service", "mysqld", "start"],
            ["chkconfig", "mysqld", "on"],
            ["mysql", "-uroot", "-e",
             "create database zabbix character set utf8 collate utf8_bin;"],
            ["mysql", "-uroot", "-e",
             "grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';"],
            ["curl", "-O", SCRIPT_URL],
            ["chmod", "+x", SCRIPT_NAME],
            ["./" + SCRIPT_NAME],
            ["rm", SCRIPT_NAME],
            ["chkconfig", "httpd", "on"],
            ["chkconfig", "zabbix-server", "on"],
            ["chkconfig", "zabbix-agent", "on"]]

    container.start()
    container.get_ips(timeout=definedvalue.TIMEOUT_VALUE)

    for arg in CMDS:
        container.attach_wait(lxc.attach_run_command, arg)

    shutdown_container(container)


def create_zabbix_server20(container_name, base):
    container = base.clone(container_name, bdevtype="aufs",
                           flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(container_name)

    RPM_URL = "http://repo.zabbix.com/zabbix/2.0/rhel/6/x86_64/zabbix-release-2.0-1.el6.noarch.rpm"
    SCRIPT_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/import_zabbixdb20.sh"
    SCRIPT_NAME = "import_zabbixdb20.sh"
    CMDS = [["rpm", "-ivh", RPM_URL],
            ["yum", "install", "-y", "mysql-server", "httpd",
             "zabbix-server-mysql", "zabbix-web-mysql", "zabbix-agent"],
            ["service", "mysqld", "start"],
            ["chkconfig", "mysqld", "on"],
            ["mysql", "-uroot", "-e",
             "create database zabbix character set utf8 collate utf8_bin;"],
            ["mysql", "-uroot", "-e",
             "grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';"],
            ["curl", "-O", SCRIPT_URL],
            ["chmod", "+x", SCRIPT_NAME],
            ["./" + SCRIPT_NAME],
            ["rm", SCRIPT_NAME],
            ["service", "httpd", "start"],
            ["chkconfig", "httpd", "on"],
            ["chkconfig", "zabbix-server", "on"],
            ["chkconfig", "zabbix-agent", "on"]]

    container.start()
    container.get_ips(timeout=definedvalue.TIMEOUT_VALUE)

    for arg in CMDS:
        container.attach_wait(lxc.attach_run_command, arg)

    shutdown_container(container)


def create_zabbix_agent22(container_name, base):
    containers = base.clone(container_name, bdevtype="aufs",
                            flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(container_name)

    RPM_URL = "http://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm"
    CMDS = [["rpm", "-ivh", RPM_URL],
            ["yum", "install", "-y", "zabbix-agent"],
            ["chkconfig", "zabbix-agent", "on"]]

    containers.start()
    containers.get_ips(timeout=definedvalue.TIMEOUT_VALUE)

    for arg in CMDS:
        container.attach_wait(lxc.attach_run_command, arg)

    shutdown_container(container)


def create_zabbix_agent20(container_name, base):
    container = base.clone(container_name, bdevtype="aufs",
                           flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(container_name)

    RPM_URL = "http://repo.zabbix.com/zabbix/2.0/rhel/6/x86_64/zabbix-release-2.0-1.el6.noarch.rpm"
    CMDS = [["rpm", "-ivh", RPM_URL],
            ["yum", "install", "-y",
             "zabbix-agent"],
            ["chkconfig", "zabbix-agent", "on"]]

    container.start()
    container.get_ips(timeout=definedvalue.TIMEOUT_VALUE)

    for arg in CMDS:
        container.attach_wait(lxc.attach_run_command, arg)

    shutdown_container(container)


def create_nagios_server3(container_name, base):
    container = base.clone(container_name, bdevtype="aufs",
                           flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(container_name)

    SCRIPT_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/import_NDOUtils3.sh"
    script_name = "import_NDOUtils3.sh"
    CMDS = [["yum", "install", "-y", "httpd", "mysql-server",
             "nagios", "nagios-plugins-all", "ndoutils-mysql"],
            ["service", "mysqld", "start"],
            ["chkconfig", "mysqld", "on"],
            ["mysql", "-uroot", "-e",
             "CREATE DATABASE ndoutils;"],
            ["mysql", "-uroot", "-e",
             "GRANT all on ndoutils.* TO ndoutils@\'%\' IDENTIFIED BY 'admin';"],
            ["curl", "-O", SCRIPT_URL],
            ["chmod", "+x", SCRIPT_NAME],
            ["./" + SCRIPT_NAME],
            ["rm", SCRIPT_NAME],
            ["chkconfig", "ndo2db", "on"],
            ["chkconfig", "nagios", "on"],
            ["chkconfig", "httpd", "on"]]

    container.start()
    container.get_ips(timeout=definedvalue.TIMEOUT_VALUE)

    for arg in CMDS:
        container.attach_wait(lxc.attach_run_command, arg)

    shutdown_container(container)


def create_nagios_server4(container_name, base):
    container = base.clone(container_name, bdevtype="aufs",
                           flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(container_name)

    NAGIOS_URL = "http://prdownloads.sourceforge.net/sourceforge/nagios/nagios-4.0.8.tar.gz"
    NAGIOS_NAME = "nagios-4.0.8.tar.gz"
    PLUGIN_URL = "http://nagios-plugins.org/download/nagios-plugins-2.0.tar.gz"
    PLUGIN_NAME = "nagios-plugins-2.0.tar.gz"
    NDOUTILS_URL = "http://downloads.sourceforge.net/project/nagios/ndoutils-2.x/ndoutils-2.0.0/ndoutils-2.0.0.tar.gz"
    NDOUTILS_NAME = "ndoutils-2.0.0.tar.gz"
    SCRIPT_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/make_Nagios4.sh"
    SCRIPT_NAME = "make_Nagios4.sh"
    CMDS = [["yum", "install", "-y", "mysql-server", "mysql-devel",
             "wget", "httpd", "php", "tar", "gcc", "glibc", "glibc-common",
             "gd", "gd-devel", "make", "net-snmp"],
            ["service", "mysqld", "start"],
            ["chkconfig", "mysqld", "on"],
            ["mysql", "-uroot", "-e",
             "CREATE DATABASE ndoutils;"],
            ["mysql", "-uroot", "-e",
             "GRANT all on ndoutils.* TO ndoutils@\'%\' IDENTIFIED BY 'admin';"],
            ["wget", NAGIOS_URL],
            ["wget", PLUGIN_URL],
            ["wget", NDOUTILS_URL],
            ["useradd", "nagios"],
            ["tar", "zxvf", NAGIOS_NAME],
            ["tar", "zxvf", PLUGIN_NAME],
            ["tar", "zxvf", NDOUTILS_NAME],
            ["curl", "-O", SCRIPT_URL],
            ["chmod", "+x", SCRIPT_NAME],
            ["./" + SCRIPT_NAME],
            ["rm", script_name]]

    container.start()
    container.get_ips(timeout=definedvalue.TIMEOUT_VALUE)

    for arg in CMDS:
        container.attach_wait(lxc.attach_run_command, arg)

    shutdown_container(container)


def create_nagios_nrpe(container_name, base):
    container = base.clone(container_name, bdevtype="aufs",
                           flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(container_name)

    CMDS = [["yum", "install", "-y", "nagios-plugins-all", "nrpe"]]

    container.start()
    container.get_ips(timeout=definedvalue.TIMEOUT_VALUE)

    for arg in CMDS:
        container.attach_wait(lxc.attach_run_command, arg)

    shutdown_container(container)


def create_hatohol_build(container_name, base):
    container = base.clone(container_name, bdevtype="aufs",
                           flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(container_name)

    REPO_URL = "https://raw.githubusercontent.com/project-hatohol/project-hatohol.github.io/master/repo/hatohol.repo"
    CUTTER_RPM = "http://sourceforge.net/projects/cutter/files/centos/cutter-release-1.1.0-0.noarch.rpm"
    CMDS = [["rpm", "-ivh", CUTTER_RPM],
            ["wget", "-P", "/etc/yum.repos.d", REPO_URL],
            ["yum", "install", "-y", "libtool", "gettext-devel",
             "glib2-devel", "libsoup-devel", "json-glib-devel",
             "sqlite-devel", "libuuid-devel", "mysql-server",
             "mysql-devel", "librabbitmq-devel", "curl",
             "qpid-cpp-client-devel","python-setuptools","python-devel",
             "Django", "httpd", "mod_wsgi", "cutter"],
            ["easy_install", "pip"],
            ["pip", "install", "mysql-python"],
            ["service", "mysqld", "start"],
            ["chkconfig", "mysqld", "on"]]

    container.start()
    container.get_ips(timeout=definedvalue.TIMEOUT_VALUE)

    for arg in CMDS:
        container.attach_wait(lxc.attach_run_command, arg)

    shutdown_container(container)


def create_hatohol_rpm(container_name, base):
    container = base.clone(container_name, bdevtype="aufs",
                           flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(container_name)

    REPO_URL = "https://raw.githubusercontent.com/project-hatohol/project-hatohol.github.io/master/repo/hatohol.repo"
    CMDS = [["yum", "install", "-y", "wget"],
            ["wget", "-P", "/etc/yum.repos.d", REPO_URL],
            ["yum", "install", "-y", "hatohol", "hatohol-client",
             "python-argparse"],
            ["chkconfig", "mysqld", "on"],
            ["service", "mysqld", "start"],
            ["hatohol-db-initiator", "hatohol", "root", ""],
            ["mysql", "-uroot", "-e"
             "CREATE DATABASE hatohol_client;"],
            ["mysql", "-uroot", "-e"
             "GRANT ALL PRIVILEGES ON hatohol_client.* TO hatohol@localhost IDENTIFIED BY 'hatohol';"],
            ["/usr/libexec/hatohol/client/manage.py", "syncdb"],
            ["chkconfig", "hatohol", "on"],
            ["chkconfig", "httpd", "on"]]

    container.start()
    container.get_ips(timeout=definedvalue.TIMEOUT_VALUE)

    for arg in CMDS:
        container.attach_wait(lxc.attach_run_command, arg)

    shutdown_container(container)


def create_fluentd(container_name, base):
    container = base.clone(container_name, bdevtype="aufs",
                           flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(container_name)

    GPG_URL = "http://packages.treasuredata.com/GPG-KEY-td-agent"
    REPO_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/fluentd.repo"
    CMDS = [["yum", "install", "-y", "wget"],
            ["rpm", "--import", GPG_URL],
            ["wget", "-P", "/etc/yum.repos.d", REPO_URL],
            ["yum", "install", "-y", "td-agent"],
            ["service", "td-agent", "start"],
            ["chkconfig", "td-agent", "on"]]

    container.start()
    container.get_ips(timeout=definedvalue.TIMEOUT_VALUE)

    for arg in CMDS:
        container.attach_wait(lxc.attach_run_command, arg)

    shutdown_container(container)


def create_redmine(container_name, base):
    container = base.clone(container_name, bdevtype="aufs",
                           flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(container_name)

    RUBY_SOURCE_URL = "http://cache.ruby-lang.org/pub/ruby/2.0/ruby-2.0.0-p481.tar.gz"
    RUBY_SOURCE_NAME = "ruby-2.0.0-p481.tar.gz"
    RUBY_INSTALL_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/install_ruby.sh"
    RUBY_INSTALL_NAME = "install_ruby.sh"
    REDMINE_TARBALL_URL = "http://www.redmine.org/releases/redmine-2.5.2.tar.gz"
    REDMINE_TARTBALL_NAME = "redmine-2.5.2.tar.gz"
    REDMINE_DIR_NAME = "redmine-2.5.2"
    PASSENGER_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/passenger.conf"
    CMDS = [["yum", "install", "-y",
             "openssl-devel", "readline-devel", "zlib-devel", "curl-devel",
             "libyaml-devel", "mysql-server", "mysql-devel", "httpd",
             "httpd-devel", "ImageMagick", "ImageMagick-devel", "wget",
             "ipa-pgothic-fonts"],
            ["curl", "-O", RUBY_INSTALL_URL],
            ["chmod", "+x", RUBY_INSTALL_NAME],
            ["curl", "-O", RUBY_SOURCE_URL],
            ["tar", "zxvf", RUBY_SOURCE_NAME],
            ["./" + RUBY_INSTALL_NAME],
            ["gem", "install", "bundler", "--no-rdoc", "--no-ri"],
            ["service", "mysqld", "start"],
            ["chkconfig", "mysqld", "on"],
            ["mysql", "-uroot", "-e",
             "CREATE DATABASE db_redmine DEFAULT CHARACTER SET utf8;"],
            ["mysql", "-uroot", "-e",
             "GRANT ALL ON db_redmine.* TO user_redmine@localhost IDENTIFIED BY \'pass_redmine\';"],
            ["curl", "-O", REDMINE_TARBALL_URL],
            ["tar", "xvf", REDMINE_TARTBALL_NAME],
            ["mv", redmine_dir_name, "/var/lib/redmine"],
            ["gem", "install", "passenger",
             "--no-rdoc", "--no-ri"],
            ["passenger-install-apache2-module", "--auto"],
            ["wget", "-P", "/etc/httpd/httpd.conf.d/", PASSENGER_URL],
            ["sed", "-i", "-e", "292d", "/etc/httpd/conf/httpd.conf"],
            ["sed", "-i", "-e",
             "291 a\\DocumentRoot /var/lib/redmine/public",
             "/etc/httpd/conf/httpd.conf"],
            ["service", "httpd", "start"],
            ["chkconfig", "httpd", "on"]]

    container.start()
    container.get_ips(timeout=definedvalue.TIMEOUT_VALUE)

    for arg in CMDS:
        container.attach_wait(lxc.attach_run_command, arg)

    shutdown_container(container)


def create_container_if_needed(key, create_function_name):
    container_name = definevalue.containers_name[key]
    base_container = lxc.Container(definevalue.containers_name["base"])
    container = lxc.Container(container_name)
    if container.defined:
        print_exists_message(container_name)
    else:
        create_function_name(container_name, base_container)


def create_base_container_if_needed():
    base_name = definevalue.containers_name["base"]
    container = lxc.Container(base_name)
    if container.defined:
        print_exists_message(base_name)
    else:
        create_base(container, base_name)


if __name__ == '__main__':
    if not os.geteuid() == 0:
        print("You need root permission to use this script.")
        sys.exit(1)

    create_base_container_if_needed()
    create_container_if_needed("zabbix_server22", create_zabbix_server22)
    create_container_if_needed("zabbix_server20", create_zabbix_server20)
    create_container_if_needed("zabbix_agent22", create_zabbix_agent22)
    create_container_if_needed("zabbix_agent20", create_zabbix_agent20)
    create_container_if_needed("nagios_server3", create_nagios_server3)
    create_container_if_needed("nagios_server4", create_nagios_server4)
    create_container_if_needed("nagios_nrpe", create_nagios_nrpe)
    create_container_if_needed("hatohol_build", create_hatohol_build)
    create_container_if_needed("hatohol_rpm", create_hatohol_rpm)
    create_container_if_needed("fluentd", create_fluentd)
    create_container_if_needed("redmine", create_redmine)
