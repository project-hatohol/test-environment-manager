#!/usr/bin/env python3
import lxc
import os
import sys
import clist

base_name = clist.containers_name["base"]
base = lxc.Container(base_name)


def print_success_message(name):
    print("Create Container: %s" % name)


def print_exists_message(name):
    print("Container already exists: %s" % name)


def create_base():
    if not base.defined:
        base.create("centos")
        print_success_message("Create Container: %s" % base_name)

        base.start()
        base.get_ips(timeout=30)
        print("Input password for root account:")
        base.attach_wait(lxc.attach_run_command,
                         ["passwd"])
        base.attach_wait(lxc.attach_run_command,
                         ["yum", "upgrade", "-y"])

        if not base.shutdown(30):
            base.stop()

    else:
        print_exists_message(base_name)


def create_zabbix_server22():
    container_name = clist.containers_name["zabbix_server22"]
    container = lxc.Container(container_name)
    if not container.defined:
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
        container.get_ips(timeout=30)

        for arg in CMDS:
            container.attach_wait(lxc.attach_run_command, arg)

        if not container.shutdown(30):
            container.stop()

    else:
        print_exists_message(container_name)


def create_zabbix_server20():
    container_name = clist.containers_name["zabbix_server20"]
    container = lxc.Container(container_name)
    if not container.defined:
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
        container.get_ips(timeout=30)

        for arg in CMDS:
            container.attach_wait(lxc.attach_run_command, arg)

        if not container.shutdown(30):
            container.stop()

    else:
        print_exists_message(container_name)


def create_zabbix_agent22():
    container_name = clist.containers_name["zabbix_agent22"]
    containers = lxc.Container(container_name)
    if not containers.defined:
        containers = base.clone(container_name, bdevtype="aufs",
                                    flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        RPM_URL = "http://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm"
        CMDS = [["rpm", "-ivh", RPM_URL],
                ["yum", "install", "-y", "zabbix-agent"],
                ["chkconfig", "zabbix-agent", "on"]]

        containers.start()
        containers.get_ips(timeout=30)

        for arg in CMDS:
            container.attach_wait(lxc.attach_run_command, arg)

        if not containers.shutdown(30):
            containers.stop()

    else:
        print_exists_message(container_name)


def create_zabbix_agent20():
    container_name = clist.containers_name["zabbix_agent20"]
    container = lxc.Container(container_name)
    if not container.defined:
        container = base.clone(container_name, bdevtype="aufs",
                                    flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        RPM_URL = "http://repo.zabbix.com/zabbix/2.0/rhel/6/x86_64/zabbix-release-2.0-1.el6.noarch.rpm"
        CMDS = [["rpm", "-ivh", RPM_URL],
                ["yum", "install", "-y",
                 "zabbix-agent"],
                ["chkconfig", "zabbix-agent", "on"]]

        container.start()
        container.get_ips(timeout=30)

        for arg in CMDS:
            container.attach_wait(lxc.attach_run_command, arg)

        if not container.shutdown(30):
            container.stop()

    else:
        print_exists_message(container_name)


def create_nagios_server3():
    container_name = clist.containers_name["nagios_server3"]
    container = lxc.Container(container_name)
    if not container.defined:
        container = base.clone(container_name, bdevtype="aufs",
                                    flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        RPM_URL = "http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
        SCRIPT_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/import_NDOUtils3.sh"
        script_name = "import_NDOUtils3.sh"
        CMDS = [["rpm", "-ivh", RPM_URL],
                ["yum", "install", "-y", "httpd", "mysql-server",
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
        container.get_ips(timeout=30)

        for arg in CMDS:
            container.attach_wait(lxc.attach_run_command, arg)

        if not container.shutdown(30):
            container.stop()

    else:
        print_exists_message(container_name)


def create_nagios_server4():
    container_name = clist.containers_name["nagios_server4"]
    container = lxc.Container(container_name)
    if not container.defined:
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
                ["yum", "groupinstall", "-y", "Development Tools"],
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
        container.get_ips(timeout=30)

        for arg in CMDS:
            container.attach_wait(lxc.attach_run_command, arg)

        if not container.shutdown(30):
            container.stop()

    else:
        print_exists_message(container_name)


def create_nagios_nrpe():
    container_name = clist.containers_name["nagios_nrpe"]
    container = lxc.Container(container_name)
    if not container.defined:
        container = base.clone(container_name, bdevtype="aufs",
                                 flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        RPM_URL = "http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
        CMDS = [["rpm", "-ivh", RPM_URL],
                ["yum", "install", "-y", "nagios-plugins-all", "nrpe"]]

        container.start()
        container.get_ips(timeout=30)

        for arg in CMDS:
            container.attach_wait(lxc.attach_run_command, arg)

        if not container.shutdown(30):
            container.stop()

    else:
        print_exists_message(container_name)


def create_hatohol_build():
    container_name = clist.containers_name["hatohol_build"]
    container = lxc.Container(container_name)
    if not container.defined:
        container = base.clone(container_name, bdevtype="aufs",
                                   flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        container.start()
        container.get_ips(timeout=30)
        REPO_URL = "https://raw.githubusercontent.com/project-hatohol/project-hatohol.github.io/master/repo/hatohol.repo"
        CUTTER_RPM = "http://sourceforge.net/projects/cutter/files/centos/cutter-release-1.1.0-0.noarch.rpm"
        container.attach_wait(lxc.attach_run_command,
                              ["rpm", "-ivh", CUTTER_RPM])
        container.attach_wait(lxc.attach_run_command,
                              ["yum", "groupinstall", "-y",
                               "Development Tools"])
        container.attach_wait(lxc.attach_run_command,
                              ["wget", "-P", "/etc/yum.repos.d", REPO_URL])
        container.attach_wait(lxc.attach_run_command,
                              ["yum", "install", "-y",
                               "libtool", "gettext-devel", "glib2-devel",
                               "libsoup-devel", "json-glib-devel",
                               "sqlite-devel", "libuuid-devel",
                               "mysql-server", "mysql-devel",
                               "librabbitmq-devel",
                               "qpid-cpp-client-devel", "curl",
                               "python-setuptools", "python-devel",
                               "Django", "httpd", "mod_wsgi", "cutter"])
        container.attach_wait(lxc.attach_run_command,
                              ["easy_install", "pip"])
        container.attach_wait(lxc.attach_run_command,
                              ["pip", "install", "mysql-python"])

        container.attach_wait(lxc.attach_run_command,
                              ["service", "mysqld", "start"])
        container.attach_wait(lxc.attach_run_command,
                              ["chkconfig", "mysqld", "on"])

        if not container.shutdown(30):
            container.stop()

    else:
        print_exists_message(container_name)


def create_hatohol_rpm():
    container_name = clist.containers_name["hatohol_rpm"]
    container = lxc.Container(container_name)
    if not container.defined:
        container = base.clone(container_name, bdevtype="aufs",
                                 flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        container.start()
        container.get_ips(timeout=30)
        REPO_URL = "https://raw.githubusercontent.com/project-hatohol/project-hatohol.github.io/master/repo/hatohol.repo"
        EPEL_URL = "http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
        container.attach_wait(lxc.attach_run_command,
                              ["yum", "install", "-y", "wget"])
        container.attach_wait(lxc.attach_run_command,
                              ["wget", "-P", "/etc/yum.repos.d", REPO_URL])
        container.attach_wait(lxc.attach_run_command,
                              ["rpm", "-ivh", EPEL_URL])
        container.attach_wait(lxc.attach_run_command,
                              ["yum", "install", "-y",
                               "hatohol", "hatohol-client",
                               "python-argparse"])

        container.attach_wait(lxc.attach_run_command,
                              ["chkconfig", "mysqld", "on"])
        container.attach_wait(lxc.attach_run_command,
                              ["service", "mysqld", "start"])
        container.attach_wait(lxc.attach_run_command,
                              ["hatohol-db-initiator", "hatohol",
                               "root", ""])
        container.attach_wait(lxc.attach_run_command,
                              ["mysql", "-uroot", "-e"
                               "CREATE DATABASE hatohol_client;"])
        container.attach_wait(lxc.attach_run_command,
                              ["mysql", "-uroot", "-e"
                               "GRANT ALL PRIVILEGES ON hatohol_client.* TO hatohol@localhost IDENTIFIED BY 'hatohol';"])
        container.attach_wait(lxc.attach_run_command,
                              ["/usr/libexec/hatohol/client/manage.py",
                               "syncdb"])

        container.attach_wait(lxc.attach_run_command,
                              ["chkconfig", "hatohol", "on"])
        container.attach_wait(lxc.attach_run_command,
                              ["chkconfig", "httpd", "on"])

        if not container.shutdown(30):
            container.stop()

    else:
        print_exists_message(container_name)


def create_fluentd():
    container_name = clist.containers_name["fluentd"]
    container = lxc.Container(container_name)
    if not container.defined:
        container = base.clone(container_name, bdevtype="aufs",
                             flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        GPG_URL = "http://packages.treasuredata.com/GPG-KEY-td-agent"
        REPO_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/fluentd.repo"
        container.start()
        container.get_ips(timeout=30)
        container.attach_wait(lxc.attach_run_command,
                              ["yum", "install", "-y", "wget"])
        container.attach_wait(lxc.attach_run_command,
                              ["rpm", "--import", GPG_URL])
        container.attach_wait(lxc.attach_run_command,
                              ["wget", "-P", "/etc/yum.repos.d", REPO_URL])
        container.attach_wait(lxc.attach_run_command,
                              ["yum", "install", "-y", "td-agent"])

        container.attach_wait(lxc.attach_run_command,
                              ["service", "td-agent", "start"])
        container.attach_wait(lxc.attach_run_command,
                              ["chkconfig", "td-agent", "on"])

        if not container.shutdown(30):
            container.stop()

    else:
        print_exists_message(container_name)


def create_redmine():
    container_name = clist.containers_name["redmine"]
    container = lxc.Container(container_name)
    if not container.defined:
        container = base.clone(container_name, bdevtype="aufs",
                             flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        RPM_URL = "http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
        RUBY_SOURCE_URL = "http://cache.ruby-lang.org/pub/ruby/2.0/ruby-2.0.0-p481.tar.gz"
        RUBY_SOURCE_NAME = "ruby-2.0.0-p481.tar.gz"
        RUBY_INSTALL_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/install_ruby.sh"
        RUBY_INSTALL_NAME = "install_ruby.sh"
        REDMINE_TARBALL_URL = "http://www.redmine.org/releases/redmine-2.5.2.tar.gz"
        REDMINE_TARTBALL_NAME = "redmine-2.5.2.tar.gz"
        REDMINE_DIR_NAME = "redmine-2.5.2"
        PASSENGER_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/passenger.conf"
        container.start()
        container.get_ips(timeout=30)
        container.attach_wait(lxc.attach_run_command,
                              ["rpm", "-ivh", RPM_URL])
        container.attach_wait(lxc.attach_run_command,
                              ["yum", "groupinstall", "-y", "Development Tools"])
        container.attach_wait(lxc.attach_run_command,
                              ["yum", "install", "-y",
                               "openssl-devel", "readline-devel", "zlib-devel",
                               "curl-devel", "libyaml-devel", "mysql-server",
                               "mysql-devel", "httpd", "httpd-devel",
                               "ImageMagick", "ImageMagick-devel",
                               "ipa-pgothic-fonts", "wget"])
        container.attach_wait(lxc.attach_run_command,
                              ["curl", "-O", RUBY_INSTALL_URL])
        container.attach_wait(lxc.attach_run_command,
                              ["chmod", "+x", RUBY_INSTALL_NAME])
        container.attach_wait(lxc.attach_run_command,
                              ["curl", "-O", RUBY_SOURCE_URL])
        container.attach_wait(lxc.attach_run_command,
                              ["tar", "zxvf", RUBY_SOURCE_NAME])
        container.attach_wait(lxc.attach_run_command,
                              ["./" + RUBY_INSTALL_NAME])
        container.attach_wait(lxc.attach_run_command,
                              ["gem", "install", "bundler", "--no-rdoc", "--no-ri"])
        container.attach_wait(lxc.attach_run_command,
                              ["service", "mysqld", "start"])
        container.attach_wait(lxc.attach_run_command,
                              ["chkconfig", "mysqld", "on"])

        container.attach_wait(lxc.attach_run_command,
                              ["mysql", "-uroot", "-e",
                               "CREATE DATABASE db_redmine DEFAULT CHARACTER SET utf8;"])
        container.attach_wait(lxc.attach_run_command,
                              ["mysql", "-uroot", "-e",
                               "GRANT ALL ON db_redmine.* TO user_redmine@localhost IDENTIFIED BY \'pass_redmine\';"])

        container.attach_wait(lxc.attach_run_command,
                              ["curl", "-O", REDMINE_TARBALL_URL])
        container.attach_wait(lxc.attach_run_command,
                              ["tar", "xvf", REDMINE_TARTBALL_NAME])
        container.attach_wait(lxc.attach_run_command,
                              ["mv", redmine_dir_name, "/var/lib/redmine"])

        container.attach_wait(lxc.attach_run_command,
                              ["gem", "install", "passenger",
                               "--no-rdoc", "--no-ri"])
        container.attach_wait(lxc.attach_run_command,
                              ["passenger-install-apache2-module", "--auto"])

        container.attach_wait(lxc.attach_run_command,
                              ["wget", "-P", "/etc/httpd/httpd.conf.d/",
                               PASSENGER_URL])

        container.attach_wait(lxc.attach_run_command,
                              ["sed", "-i", "-e", "292d",
                               "/etc/httpd/conf/httpd.conf"])
        container.attach_wait(lxc.attach_run_command,
                              ["sed", "-i", "-e",
                               "291 a\\DocumentRoot /var/lib/redmine/public",
                               "/etc/httpd/conf/httpd.conf"])

        container.attach_wait(lxc.attach_run_command,
                              ["service", "httpd", "start"])
        container.attach_wait(lxc.attach_run_command,
                              ["chkconfig", "httpd", "on"])

        if not container.shutdown(30):
            container.stop()

    else:
        print_exists_message(container_name)


if __name__ == '__main__':
    if not os.geteuid() == 0:
        print("You need root permission to use this script.")
        sys.exit(1)

    create_base()
    create_zabbix_server22()
    create_zabbix_server20()
    create_zabbix_agent22()
    create_zabbix_agent20()
    create_nagios_server3()
    create_nagios_server4()
    create_nagios_nrpe()
    create_hatohol_build()
    create_hatohol_rpm()
    create_fluentd()
    create_redmine()
