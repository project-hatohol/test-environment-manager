#!/usr/bin/env python3
import lxc
import os
import sys

base_name = "env_base"
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
        base.attach_wait(lxc.attach_run_command,
                         ["yum", "upgrade", "-y"])

        if not base.shutdown(30):
            base.stop()

    else:
        print_exists_message(base_name)


def create_zabbix_server22():
    container_name = "env_zabbix_server22"
    zabbix_server22 = lxc.Container(container_name)
    if not zabbix_server22.defined:
        zabbix_server22 = base.clone(container_name, bdevtype="aufs",
                                     flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        rpm_url = "http://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm"
        script_url = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/import_zabbixdb22.sh"
        script_name = "import_zabbixdb22.sh"
        zabbix_server22.start()
        zabbix_server22.get_ips(timeout=30)
        zabbix_server22.attach_wait(lxc.attach_run_command,
                                    ["rpm", "-ivh", rpm_url])
        zabbix_server22.attach_wait(lxc.attach_run_command,
                                    ["yum", "install", "-y",
                                     "mysql-server", "httpd",
                                     "zabbix-server-mysql",
                                     "zabbix-web-mysql"])

        zabbix_server22.attach_wait(lxc.attach_run_command,
                                    ["service", "mysqld", "start"])
        zabbix_server22.attach_wait(lxc.attach_run_command,
                                    ["chkconfig", "mysqld", "on"])

        zabbix_server22.attach_wait(lxc.attach_run_command,
                                    ["mysql", "-uroot", "-e",
                                     "create database zabbix character set utf8 collate utf8_bin;"])
        zabbix_server22.attach_wait(lxc.attach_run_command,
                                    ["mysql", "-uroot", "-e",
                                     "grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';"])

        zabbix_server22.attach_wait(lxc.attach_run_command,
                                    ["curl", "-O", script_url])
        zabbix_server22.attach_wait(lxc.attach_run_command,
                                    ["chmod", "+x", script_name])
        zabbix_server22.attach_wait(lxc.attach_run_command,
                                    ["./" + script_name])
        zabbix_server22.attach_wait(lxc.attach_run_command,
                                    ["rm", script_name])

        zabbix_server22.attach_wait(lxc.attach_run_command,
                                    ["service", "httpd", "start"])
        zabbix_server22.attach_wait(lxc.attach_run_command,
                                    ["chkconfig", "httpd", "on"])
        zabbix_server22.attach_wait(lxc.attach_run_command,
                                    ["chkconfig", "zabbix-server", "on"])

        if not zabbix_server22.shutdown(30):
            zabbix_server22.stop()

    else:
        print_exists_message(container_name)


def create_zabbix_server20():
    container_name = "env_zabbix_server20"
    zabbix_server20 = lxc.Container(container_name)
    if not zabbix_server20.defined:
        zabbix_server20 = base.clone(container_name, bdevtype="aufs",
                                     flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        rpm_url = "http://repo.zabbix.com/zabbix/2.0/rhel/6/x86_64/zabbix-release-2.0-1.el6.noarch.rpm"
        script_url = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/import_zabbixdb20.sh"
        script_name = "import_zabbixdb20.sh"
        zabbix_server20.start()
        zabbix_server20.get_ips(timeout=30)
        zabbix_server20.attach_wait(lxc.attach_run_command,
                                    ["rpm", "-ivh", rpm_url])
        zabbix_server20.attach_wait(lxc.attach_run_command,
                                    ["yum", "install", "-y",
                                     "mysql-server", "httpd",
                                     "zabbix-server-mysql",
                                     "zabbix-web-mysql"])

        zabbix_server20.attach_wait(lxc.attach_run_command,
                                    ["service", "mysqld", "start"])
        zabbix_server20.attach_wait(lxc.attach_run_command,
                                    ["chkconfig", "mysqld", "on"])

        zabbix_server20.attach_wait(lxc.attach_run_command,
                                    ["mysql", "-uroot", "-e",
                                     "create database zabbix character set utf8 collate utf8_bin;"])
        zabbix_server20.attach_wait(lxc.attach_run_command,
                                    ["mysql", "-uroot", "-e",
                                     "grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';"])

        zabbix_server20.attach_wait(lxc.attach_run_command,
                                    ["curl", "-O", script_url])
        zabbix_server20.attach_wait(lxc.attach_run_command,
                                    ["chmod", "+x", script_name])
        zabbix_server20.attach_wait(lxc.attach_run_command,
                                    ["./" + script_name])
        zabbix_server20.attach_wait(lxc.attach_run_command,
                                    ["rm", script_name])

        zabbix_server20.attach_wait(lxc.attach_run_command,
                                    ["service", "httpd", "start"])
        zabbix_server20.attach_wait(lxc.attach_run_command,
                                    ["chkconfig", "httpd", "on"])
        zabbix_server20.attach_wait(lxc.attach_run_command,
                                    ["chkconfig", "zabbix-server", "on"])

        if not zabbix_server20.shutdown(30):
            zabbix_server20.stop()

    else:
        print_exists_message(container_name)


def create_zabbix_agent22():
    container_name = "env_zabbix_agent22"
    zabbix_agent22 = lxc.Container(container_name)
    if not zabbix_agent22.defined:
        zabbix_agent22 = base.clone(container_name, bdevtype="aufs",
                                    flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        rpm_url = "http://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm"
        zabbix_agent22.start()
        zabbix_agent22.get_ips(timeout=30)
        zabbix_agent22.attach_wait(lxc.attach_run_command,
                                   ["rpm", "-ivh", rpm_url])
        zabbix_agent22.attach_wait(lxc.attach_run_command,
                                   ["yum", "install", "-y",
                                    "zabbix-agent"])

        zabbix_agent22.attach_wait(lxc.attach_run_command,
                                   ["chkconfig", "zabbix-agent", "on"])

        if not zabbix_agent22.shutdown(30):
            zabbix_agent22.stop()

    else:
        print_exists_message(container_name)


def create_zabbix_agent20():
    container_name = "env_zabbix_agent20"
    zabbix_agent20 = lxc.Container(container_name)
    if not zabbix_agent20.defined:
        zabbix_agent20 = base.clone(container_name, bdevtype="aufs",
                                    flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        rpm_url = "http://repo.zabbix.com/zabbix/2.0/rhel/6/x86_64/zabbix-release-2.0-1.el6.noarch.rpm"
        zabbix_agent20.start()
        zabbix_agent20.get_ips(timeout=30)
        zabbix_agent20.attach_wait(lxc.attach_run_command,
                                   ["rpm", "-ivh", rpm_url])
        zabbix_agent20.attach_wait(lxc.attach_run_command,
                                   ["yum", "install", "-y",
                                    "zabbix-agent"])

        zabbix_agent20.attach_wait(lxc.attach_run_command,
                                   ["chkconfig", "zabbix-agent", "on"])

        if not zabbix_agent20.shutdown(30):
            zabbix_agent20.stop()

    else:
        print_exists_message(container_name)


def create_nagios_server3():
    container_name = "env_nagios_server3"
    nagios_server3 = lxc.Container(container_name)
    if not nagios_server3.defined:
        nagios_server3 = base.clone(container_name, bdevtype="aufs",
                                    flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        rpm_url = "http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
        script_url = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/import_NDOUtils3.sh"
        script_name = "import_NDOUtils3.sh"
        nagios_server3.start()
        nagios_server3.get_ips(timeout=30)
        nagios_server3.attach_wait(lxc.attach_run_command,
                                   ["rpm", "-ivh", rpm_url])
        nagios_server3.attach_wait(lxc.attach_run_command,
                                   ["yum", "install", "-y",
                                    "httpd", "mysql-server",
                                    "nagios", "nagios-plugins-all",
                                    "ndoutils-mysql"])
        nagios_server3.attach_wait(lxc.attach_run_command,
                                   ["service", "mysqld", "start"])
        nagios_server3.attach_wait(lxc.attach_run_command,
                                   ["chkconfig", "mysqld", "on"])

        nagios_server3.attach_wait(lxc.attach_run_command,
                                   ["mysql", "-uroot", "-e",
                                    "CREATE DATABASE ndoutils;"])
        nagios_server3.attach_wait(lxc.attach_run_command,
                                   ["mysql", "-uroot", "-e",
                                    "GRANT all on ndoutils.* TO ndoutils@\'%\' IDENTIFIED BY 'admin';"])

        nagios_server3.attach_wait(lxc.attach_run_command,
                                   ["curl", "-O", script_url])
        nagios_server3.attach_wait(lxc.attach_run_command,
                                   ["chmod", "+x", script_name])
        nagios_server3.attach_wait(lxc.attach_run_command,
                                   ["./" + script_name])
        nagios_server3.attach_wait(lxc.attach_run_command,
                                   ["rm", script_name])

        nagios_server3.attach_wait(lxc.attach_run_command,
                                   ["chkconfig", "ndo2db", "on"])
        nagios_server3.attach_wait(lxc.attach_run_command,
                                   ["chkconfig", "nagios", "on"])
        nagios_server3.attach_wait(lxc.attach_run_command,
                                   ["chkconfig", "httpd", "on"])

        if not nagios_server3.shutdown(30):
            nagios_server3.stop()

    else:
        print_exists_message(container_name)


def create_nagios_server4():
    container_name = "env_nagios_server4"
    nagios_server4 = lxc.Container(container_name)
    if not nagios_server4.defined:
        nagios_server4 = base.clone(container_name, bdevtype="aufs",
                                    flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        nagios_url = "http://prdownloads.sourceforge.net/sourceforge/nagios/nagios-4.0.8.tar.gz"
        nagios_name = "nagios-4.0.8.tar.gz"
        plugin_url = "http://nagios-plugins.org/download/nagios-plugins-2.0.tar.gz"
        plugin_name = "nagios-plugins-2.0.tar.gz"
        ndoutils_url = "http://downloads.sourceforge.net/project/nagios/ndoutils-2.x/ndoutils-2.0.0/ndoutils-2.0.0.tar.gz"
        ndoutils_name = "ndoutils-2.0.0.tar.gz"
        script_url = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/make_Nagios4.sh"
        script_name = "make_Nagios4.sh"
        nagios_server4.start()
        nagios_server4.get_ips(timeout=30)
        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["yum", "install", "-y",
                                    "mysql-server", "mysql-devel",
                                    "wget", "httpd", "php", "tar",
                                    "gcc", "glibc", "glibc-common",
                                    "gd", "gd-devel", "make", "net-snmp"])
        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["yum", "groupinstall", "-y",
                                    "Development Tools"])
        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["service", "mysqld", "start"])
        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["chkconfig", "mysqld", "on"])

        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["mysql", "-uroot", "-e",
                                    "CREATE DATABASE ndoutils;"])
        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["mysql", "-uroot", "-e",
                                    "GRANT all on ndoutils.* TO ndoutils@\'%\' IDENTIFIED BY 'admin';"])

        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["wget", nagios_url])
        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["wget", plugin_url])
        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["wget", ndoutils_url])
        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["useradd", "nagios"])

        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["tar", "zxvf", nagios_name])
        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["tar", "zxvf", plugin_name])
        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["tar", "zxvf", ndoutils_name])

        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["curl", "-O", script_url])
        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["chmod", "+x", script_name])
        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["./" + script_name])
        nagios_server4.attach_wait(lxc.attach_run_command,
                                   ["rm", script_name])

        if not nagios_server4.shutdown(30):
            nagios_server4.stop()

    else:
        print_exists_message(container_name)


def create_nagios_nrpe():
    container_name = "env_nagios_nrpe"
    nagios_nrpe = lxc.Container(container_name)
    if not nagios_nrpe.defined:
        nagios_nrpe = base.clone(container_name, bdevtype="aufs",
                                 flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        rpm_url = "http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
        nagios_nrpe.start()
        nagios_nrpe.get_ips(timeout=30)
        nagios_nrpe.attach_wait(lxc.attach_run_command,
                                ["rpm", "-ivh", rpm_url])
        nagios_nrpe.attach_wait(lxc.attach_run_command,
                                ["yum", "install", "-y",
                                 "nagios-plugins-all"])

        if not nagios_nrpe.shutdown(30):
            nagios_nrpe.stop()

    else:
        print_exists_message(container_name)


def create_hatohol_build():
    container_name = "env_hatohol_build"
    hatohol_build = lxc.Container(container_name)
    if not hatohol_build.defined:
        hatohol_build = base.clone(container_name, bdevtype="aufs",
                                   flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        hatohol_build.start()
        hatohol_build.get_ips(timeout=30)
        repo_url = "https://raw.githubusercontent.com/project-hatohol/project-hatohol.github.io/master/repo/hatohol.repo"
        cutter_rpm = "http://sourceforge.net/projects/cutter/files/centos/cutter-release-1.1.0-0.noarch.rpm"
        hatohol_build.attach_wait(lxc.attach_run_command,
                                  ["rpm", "-ivh", cutter_rpm])
        hatohol_build.attach_wait(lxc.attach_run_command,
                                  ["yum", "groupinstall", "-y",
                                   "Development Tools"])
        hatohol_build.attach_wait(lxc.attach_run_command,
                                  ["wget", "-P", "/etc/yum.repos.d", repo_url])
        hatohol_build.attach_wait(lxc.attach_run_command,
                                  ["yum", "install", "-y",
                                   "libtool", "gettext-devel", "glib2-devel",
                                   "libsoup-devel", "json-glib-devel",
                                   "sqlite-devel", "libuuid-devel",
                                   "mysql-server", "mysql-devel",
                                   "librabbitmq-devel",
                                   "qpid-cpp-client-devel", "curl",
                                   "python-setuptools", "python-devel",
                                   "Django", "httpd", "mod_wsgi", "cutter"])
        hatohol_build.attach_wait(lxc.attach_run_command,
                                  ["easy_install", "pip"])
        hatohol_build.attach_wait(lxc.attach_run_command,
                                  ["pip", "install", "mysql-python"])

        hatohol_build.attach_wait(lxc.attach_run_command,
                                  ["service", "mysqld", "start"])
        hatohol_build.attach_wait(lxc.attach_run_command,
                                  ["chkconfig", "mysqld", "on"])

        if not hatohol_build.shutdown(30):
            hatohol_build.stop()

    else:
        print_exists_message(container_name)


def create_hatohol_rpm():
    container_name = "env_hatohol_rpm"
    hatohol_rpm = lxc.Container(container_name)
    if not hatohol_rpm.defined:
        hatohol_rpm = base.clone(container_name, bdevtype="aufs",
                                 flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        hatohol_rpm.start()
        hatohol_rpm.get_ips(timeout=30)
        repo_url = "https://raw.githubusercontent.com/project-hatohol/project-hatohol.github.io/master/repo/hatohol.repo"
        hatohol_rpm.attach_wait(lxc.attach_run_command,
                                ["yum", "install", "-y", "wget"])
        hatohol_rpm.attach_wait(lxc.attach_run_command,
                                ["wget", "-P", "/etc/yum.repos.d", repo_url])
        hatohol_rpm.attach_wait(lxc.attach_run_command,
                                ["yum", "install", "-y",
                                 "hatohol", "hatohol-client"])

        hatohol_rpm.attach_wait(lxc.attach_run_command,
                                ["chkconfig", "mysqld", "on"])
        hatohol_rpm.attach_wait(lxc.attach_run_command,
                                ["service", "mysqld", "start"])
        # TODO: Add Process after 14.09 is released.

        if not hatohol_rpm.shutdown(30):
            hatohol_rpm.stop()

    else:
        print_exists_message(container_name)


def create_fluentd():
    container_name = "env_fluentd"
    fluentd = lxc.Container(container_name)
    if not fluentd.defined:
        fluentd = base.clone(container_name, bdevtype="aufs",
                             flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        GPG_url = "http://packages.treasuredata.com/GPG-KEY-td-agent"
        repo_url = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/fluentd.repo"
        fluentd.start()
        fluentd.get_ips(timeout=30)
        fluentd.attach_wait(lxc.attach_run_command,
                            ["yum", "install", "-y", "wget"])
        fluentd.attach_wait(lxc.attach_run_command,
                            ["rpm", "--import", GPG_url])
        fluentd.attach_wait(lxc.attach_run_command,
                            ["wget", "-P", "/etc/yum.repos.d", repo_url])
        fluentd.attach_wait(lxc.attach_run_command,
                            ["yum", "install", "-y", "td-agent"])

        fluentd.attach_wait(lxc.attach_run_command,
                            ["service", "td-agent", "start"])
        fluentd.attach_wait(lxc.attach_run_command,
                            ["chkconfig", "td-agent", "on"])

        if not fluentd.shutdown(30):
            fluentd.stop()

    else:
        print_exists_message(container_name)


def create_redmine():
    container_name = "env_redmine"
    redmine = lxc.Container(container_name)
    if not redmine.defined:
        redmine = base.clone(container_name, bdevtype="aufs",
                             flags=lxc.LXC_CLONE_SNAPSHOT)
        print_success_message(container_name)

        rpm_url = "http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
        ruby_source_url = "http://cache.ruby-lang.org/pub/ruby/2.0/ruby-2.0.0-p481.tar.gz"
        ruby_source_name = "ruby-2.0.0-p481.tar.gz"
        ruby_install_url = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/install_ruby.sh"
        ruby_install_name = "install_ruby.sh"
        redmine_tarball_url = "http://www.redmine.org/releases/redmine-2.5.2.tar.gz"
        redmine_tartball_name = "redmine-2.5.2.tar.gz"
        redmine_dir_name = "redmine-2.5.2"
        passenger_url = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/creator/creator/script/passenger.conf"
        redmine.start()
        redmine.get_ips(timeout=30)
        redmine.attach_wait(lxc.attach_run_command,
                            ["rpm", "-ivh", rpm_url])
        redmine.attach_wait(lxc.attach_run_command,
                            ["yum", "groupinstall", "-y", "Development Tools"])
        redmine.attach_wait(lxc.attach_run_command,
                            ["yum", "install", "-y",
                             "openssl-devel", "readline-devel", "zlib-devel",
                             "curl-devel", "libyaml-devel", "mysql-server",
                             "mysql-devel", "httpd", "httpd-devel",
                             "ImageMagick", "ImageMagick-devel",
                             "ipa-pgothic-fonts", "wget"])
        redmine.attach_wait(lxc.attach_run_command,
                            ["curl", "-O", ruby_install_url])
        redmine.attach_wait(lxc.attach_run_command,
                            ["chmod", "+x", ruby_install_name])
        redmine.attach_wait(lxc.attach_run_command,
                            ["curl", "-O", ruby_source_url])
        redmine.attach_wait(lxc.attach_run_command,
                            ["tar", "zxvf", ruby_source_name])
        redmine.attach_wait(lxc.attach_run_command,
                            ["./" + ruby_install_name])
        redmine.attach_wait(lxc.attach_run_command,
                            ["gem", "install", "bundler", "--no-rdoc", "--no-ri"])
        redmine.attach_wait(lxc.attach_run_command,
                            ["service", "mysqld", "start"])
        redmine.attach_wait(lxc.attach_run_command,
                            ["chkconfig", "mysqld", "on"])

        redmine.attach_wait(lxc.attach_run_command,
                            ["mysql", "-uroot", "-e",
                             "CREATE DATABASE db_redmine DEFAULT CHARACTER SET utf8;"])
        redmine.attach_wait(lxc.attach_run_command,
                            ["mysql", "-uroot", "-e",
                             "GRANT ALL ON db_redmine.* TO user_redmine@localhost IDENTIFIED BY \'pass_redmine\';"])

        redmine.attach_wait(lxc.attach_run_command,
                            ["curl", "-O", redmine_tarball_url])
        redmine.attach_wait(lxc.attach_run_command,
                            ["tar", "xvf", redmine_tartball_name])
        redmine.attach_wait(lxc.attach_run_command,
                            ["mv", redmine_dir_name, "/var/lib/redmine"])

        redmine.attach_wait(lxc.attach_run_command,
                            ["gem", "install", "passenger",
                             "--no-rdoc", "--no-ri"])
        redmine.attach_wait(lxc.attach_run_command,
                            ["passenger-install-apache2-module", "--auto"])

        redmine.attach_wait(lxc.attach_run_command,
                            ["wget", "-P", "/etc/httpd/httpd.conf.d/",
                             passenger_url])

        redmine.attach_wait(lxc.attach_run_command,
                            ["sed", "-i", "-e", "292d",
                             "/etc/httpd/conf/httpd.conf"])
        redmine.attach_wait(lxc.attach_run_command,
                            ["sed", "-i", "-e",
                             "291 a\\DocumentRoot /var/lib/redmine/public",
                             "/etc/httpd/conf/httpd.conf"])

        redmine.attach_wait(lxc.attach_run_command,
                            ["service", "httpd", "start"])
        redmine.attach_wait(lxc.attach_run_command,
                            ["chkconfig", "httpd", "on"])

    if not redmine.shutdown(30):
        redmine.stop()

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
