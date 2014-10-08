#!/usr/bin/env python3
import os
import sys
import lxc
sys.path.append("../common")
import definevalue
from utils import *

def run_commands_in_container(container, cmds):
    for command in cmds:
        container.attach_wait(lxc.attach_run_command, command)


def clone_start_container(container_name, base):
    container = base.clone(container_name, bdevtype="aufs",
                           flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(container_name)

    container.start()
    container.get_ips(timeout=definevalue.TIMEOUT_VALUE)

    return container


def create_base(container, container_name):
    container.create("centos")
    print_success_message(container_name)

    EPEL_URL = "http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
    CMDS = [["yum", "upgrade", "-y"],
            ["yum", "groupinstall", "-y", "Development Tools"],
            ["yum", "install", "-y", "wget"],
            ["rpm", "-ivh", EPEL_URL]]

    container.start()
    container.get_ips(timeout=definevalue.TIMEOUT_VALUE)
    print("Input password for root account:")
    container.attach_wait(lxc.attach_run_command, ["passwd"])

    run_commands_in_container(container, CMDS)
    shutdown_container(container)


def clone_container_and_install_software(container_name, base, cmds):
    container = clone_start_container(container_name, base)
    run_commands_in_container(container, cmds)
    shutdown_container(container)


def get_commands_to_install_zabbix_server22():
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

    return CMDS


def get_commands_to_install_zabbix_server20():
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

    return CMDS


def get_commands_to_install_zabbix_agent22():
    RPM_URL = "http://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm"
    CMDS = [["rpm", "-ivh", RPM_URL],
            ["yum", "install", "-y", "zabbix-agent"],
            ["chkconfig", "zabbix-agent", "on"]]

    return CMDS


def get_commands_to_install_zabbix_agent20():
    RPM_URL = "http://repo.zabbix.com/zabbix/2.0/rhel/6/x86_64/zabbix-release-2.0-1.el6.noarch.rpm"
    CMDS = [["rpm", "-ivh", RPM_URL],
            ["yum", "install", "-y",
             "zabbix-agent"],
            ["chkconfig", "zabbix-agent", "on"]]

    return CMDS


def get_commands_to_install_nagios_server3():
    SCRIPT_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/import_NDOUtils3.sh"
    SCRIPT_NAME = "import_NDOUtils3.sh"
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

    return CMDS


def get_commands_to_install_nagios_server4():
    NAGIOS_URL = "http://prdownloads.sourceforge.net/sourceforge/nagios/nagios-4.0.8.tar.gz"
    NAGIOS_NAME = "nagios-4.0.8.tar.gz"
    PLUGIN_URL = "http://nagios-plugins.org/download/nagios-plugins-2.0.tar.gz"
    PLUGIN_NAME = "nagios-plugins-2.0.tar.gz"
    NDOUTILS_URL = "http://downloads.sourceforge.net/project/nagios/ndoutils-2.x/ndoutils-2.0.0/ndoutils-2.0.0.tar.gz"
    NDOUTILS_NAME = "ndoutils-2.0.0.tar.gz"
    SCRIPT_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/make_Nagios4.sh"
    SCRIPT_NAME = "make_Nagios4.sh"
    CMDS = [["yum", "install", "-y", "mysql-server", "mysql-devel",
             "httpd", "php", "tar", "gcc", "glibc", "glibc-common",
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
            ["rm", SCRIPT_NAME]]

    return CMDS


def get_commands_to_install_nagios_nrpe():
    CMDS = [["yum", "install", "-y", "nagios-plugins-all", "nrpe"]]

    return CMDS


def get_commands_to_install_packages_for_building_hatohol():
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

    return CMDS


def get_commands_to_install_hatohol():
    REPO_URL = "https://raw.githubusercontent.com/project-hatohol/project-hatohol.github.io/master/repo/hatohol.repo"
    CMDS = [["wget", "-P", "/etc/yum.repos.d", REPO_URL],
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

    return CMDS


def get_commands_to_install_fluentd():
    GPG_URL = "http://packages.treasuredata.com/GPG-KEY-td-agent"
    REPO_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/fluentd.repo"
    CMDS = [["rpm", "--import", GPG_URL],
            ["wget", "-P", "/etc/yum.repos.d", REPO_URL],
            ["yum", "install", "-y", "td-agent"],
            ["service", "td-agent", "start"],
            ["chkconfig", "td-agent", "on"]]

    return CMDS


def get_commands_to_install_redmine():
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
             "httpd-devel", "ImageMagick", "ImageMagick-devel",
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
            ["mv", REDMINE_DIR_NAME, "/var/lib/redmine"],
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

    return CMDS


def create_container_if_needed(container_name, get_commands_function_name):
    if not is_container_name_defined(container_name):
        return

    base_container = lxc.Container("env_base")
    container = lxc.Container(container_name)
    if container.defined:
        print_exists_message(container_name)
    else:
        cmds = get_commands_function_name()
        clone_container_and_install_software(container_name, base_container, cmds)


def create_base_container_if_needed():
    base_name = "env_base"
    if not is_container_name_defined(base_name):
        return False

    container = lxc.Container(base_name)
    if container.defined:
        print_exists_message(base_name)
    else:
        create_base(container, base_name)

    return True


def create_containers():
    ARGS = [["env_zabbix_server22", get_commands_to_install_zabbix_server22],
            ["env_zabbix_server20", get_commands_to_install_zabbix_server20],
            ["env_zabbix_agent22", get_commands_to_install_zabbix_agent22],
            ["env_zabbix_agent20", get_commands_to_install_zabbix_agent20],
            ["env_nagios_server3", get_commands_to_install_nagios_server3],
            ["env_nagios_server4", get_commands_to_install_nagios_server4],
            ["env_nagios_nrpe", get_commands_to_install_nagios_nrpe],
            ["env_hatohol_build", get_commands_to_install_packages_for_building_hatohol],
            ["env_hatohol_rpm", get_commands_to_install_hatohol],
            ["env_fluentd", get_commands_to_install_fluentd],
            ["env_redmine", get_commands_to_install_redmine]]

    if not create_base_container_if_needed():
        return

    for (container_name, get_commands_function_name) in ARGS:
        create_container_if_needed(container_name, get_commands_function_name)


if __name__ == '__main__':
    exit_if_user_run_this_as_general_user()

    create_containers()
