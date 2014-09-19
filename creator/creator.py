#!/usr/bin/env python3
import lxc
import os
import sys

def print_success_message(name):
    print("Create Container: %s" % name)


if not os.geteuid() == 0:
    print("You need root permission to use this script.")
    sys.exit(1)


base_name = "env_base"
base = lxc.Container(base_name)
if not base.defined:
    base.create("centos")
    print_success_message("Create Container: %s" % base_name)

    base.start()
    base.get_ips(timeout=30)
    base.attach_wait(lxc.attach_run_command,
                     ["yum", "upgrade", "-y"])

    if not base.shutdown(30):
        base.stop()


zabbix_server22_name = "env_zabbix_server22"
zabbix_server22 = lxc.Container(zabbix_server22_name)
if not zabbix_server22.defined:
    zabbix_server22 = base.clone(zabbix_server22_name, bdevtype="aufs",
                                 flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(zabbix_server22_name)

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


zabbix_server20_name = "env_zabbix_server20"
zabbix_server20 = lxc.Container(zabbix_server20_name)
if not zabbix_server20.defined:
    zabbix_server20 = base.clone(zabbix_server20_name, bdevtype="aufs",
                                 flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(zabbix_server20_name)

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


zabbix_agent22_name = "env_zabbix_agent22"
zabbix_agent22 = lxc.Container(zabbix_agent22_name)
if not zabbix_agent22.defined:
    zabbix_agent22 = base.clone(zabbix_agent22_name, bdevtype="aufs",
                                 flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(zabbix_agent22_name)

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


zabbix_agent20_name = "env_zabbix_agent20"
zabbix_agent20 = lxc.Container(zabbix_agent20_name)
if not zabbix_agent20.defined:
    zabbix_agent20 = base.clone(zabbix_agent20_name, bdevtype="aufs",
                                 flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(zabbix_agent20_name)

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


nagios_server3_name = "env_nagios_server3"
nagios_server3 = lxc.Container(nagios_server3_name)
if not nagios_server3.defined:
    nagios_server3 = base.clone(nagios_server3_name, bdevtype="aufs",
                                 flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(nagios_server3_name)

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


nagios_server4_name = "env_nagios_server4"
nagios_server4 = lxc.Container(nagios_server4_name)
if not nagios_server4.defined:
    nagios_server4 = base.clone(nagios_server4_name, bdevtype="aufs",
                                 flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(nagios_server4_name)

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


nagios_nrpe_name = "env_nagios_nrpe"
nagios_nrpe = lxc.Container(nagios_nrpe_name)
if not nagios_nrpe.defined:
    nagios_nrpe = base.clone(nagios_nrpe_name, bdevtype="aufs",
                             flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(nagios_nrpe_name)

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


hatohol_build_name = "env_hatohol_build"
hatohol_build = lxc.Container(hatohol_build_name)
if not hatohol_build.defined:
    hatohol_build = base.clone(hatohol_build_name, bdevtype="aufs",
                               flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(hatohol_build_name)

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


hatohol_rpm_name = "env_hatohol_rpm"
hatohol_rpm = lxc.Container(hatohol_rpm_name)
if not hatohol_rpm.defined:
    hatohol_rpm = base.clone(hatohol_rpm_name, bdevtype="aufs",
                             flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(hatohol_rpm_name)

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


fluentd_name = "env_fluentd"
fluentd = lxc.Container(fluentd_name)
if not fluentd.defined:
    fluentd = base.clone(fluentd_name, bdevtype="aufs",
                         flags=lxc.LXC_CLONE_SNAPSHOT)
    print_success_message(fluentd_name)

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
