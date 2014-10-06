#!/usr/bin/env python3
import lxc
import os
import sys
import os.path
import definevalue
from utils import *

def check_container_exist():
    NAMES = ["env_base", "env_zabbix_server22", "env_zabbix_server20",
             "env_zabbix_agent22", "env_zabbix_agent20",
             "env_nagios_server3", "env_nagios_server4",
             "env_nagios_nrpe", "env_hatohol_build",
             "env_hatohol_rpm", "env_fluentd", "env_redmine"]

    for container_name in NAMES:
        if not is_container_name_defined(container_name):
            return False

        if lxc.Container(container_name).defined:
            print("Container \"%s\": True" % container_name)
        else:
            print("Container \"%s\": False" % container_name)
            return False

    print_new_line()
    return True


def print_file_is_usable(file_path):
    if os.path.isfile(file_path):
        print("\"%s\" file exists: True" % file_path)
    else:
        print("\"%s\" file exists: False" % file_path)


def print_directory_is_usable(directory_path):
    if os.path.isdir(directory_path):
        print("\"%s\" directory exists: True" % directory_path)
    else:
        print("\"%s\" directory exists: False" % directory_path)


def run_check_command(container, check_item):
    for (function_name, argument) in check_item:
        container.attach_wait(function_name, argument)


def check_container(container_name, check_item):
    container = lxc.Container(container_name)
    print("Container name: %s" % container_name)

    container.start()
    run_check_command(container, check_item)
    shutdown_container(container)


def check_zabbix_server_container(container_name):
    CHECK_ITEM = [[print_file_is_usable, "/usr/sbin/zabbix_server"],
                  [print_file_is_usable, "/usr/sbin/zabbix_agentd"]]

    check_container(container_name, CHECK_ITEM)


def check_zabbix_agent_container(container_name):
    CHECK_ITEM = [[print_file_is_usable, "/usr/sbin/zabbix_agentd"]]

    check_container(container_name, CHECK_ITEM)


def check_nagios_server3_container():
    CHECK_ITEM = [[print_file_is_usable, "/usr/sbin/nagios"],
                  [print_file_is_usable, "/usr/sbin/ndo2db"]]
    container_name = "env_nagios_server3"

    check_container(container_name, CHECK_ITEM)


def check_nagios_server4_container():
    CHECK_ITEM = [[print_file_is_usable, "/usr/local/nagios/bin/nagios"],
                  [print_file_is_usable, "/usr/local/nagios/bin/ndo2db"]]
    container_name = "env_nagios_server4"

    check_container(container_name, CHECK_ITEM)


def check_nagios_nrpe_container():
    CHECK_ITEM = [[print_file_is_usable, "/etc/nagios/nrpe.cfg"],
                  [print_directory_is_usable, "/usr/lib64/nagios/plugins/"]]
    container_name = "env_nagios_nrpe"

    check_container(container_name, CHECK_ITEM)


def check_hatohol_container():
    CHECK_ITEM = [[print_file_is_usable, "/usr/sbin/hatohol"]]
    container_name = "env_hatohol_rpm"

    check_container(container_name, CHECK_ITEM)


def check_redmine_container():
    CHECK_ITEM = [[print_directory_is_usable, "/var/lib/redmine"],
                  [print_file_is_usable, "/usr/local/bin/ruby"]]
    container_name = "env_redmine"

    check_container(container_name, CHECK_ITEM)


def check_fluentd_container():
    CHECK_ITEM = [[print_file_is_usable, "/usr/sbin/td-agent"]]
    container_name = "env_fluentd"

    check_container(container_name, CHECK_ITEM)


def check_container_successfully():
    check_hatohol_container()
    check_zabbix_server_container("env_zabbix_server22")
    check_zabbix_server_container("env_zabbix_server20")
    check_zabbix_agent_container("env_zabbix_agent22")
    check_zabbix_agent_container("env_zabbix_agent20")
    check_nagios_server3_container()
    check_nagios_server4_container()
    check_nagios_nrpe_container()
    check_redmine_container()
    check_fluentd_container()


if __name__ == '__main__':
    if not os.geteuid() == 0:
        print("You need root permission to use this script.")
        sys.exit(1)

    if check_container_exist():
        check_container_successfully()
