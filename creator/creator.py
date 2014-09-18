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
