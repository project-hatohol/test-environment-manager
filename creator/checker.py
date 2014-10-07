#!/usr/bin/env python3
import lxc
import os
import sys
import os.path
import definevalue
from utils import *

def check_container_exist():
    for container_name in definevalue.CONTAINER_NAME:
        if lxc.Container(container_name).defined:
            print("Container \"%s\": True" % container_name)
        else:
            print("Container \"%s\": False" % container_name)
            return False

    print_new_line()
    return True


def print_file_is_usable(file_path):
    print("\"%s\" file exists: %s" % file_path, os.path.isfile(file_path))


def print_directory_is_usable(directory_path):
    print("\"%s\" directory exists: %s" % directory_path, os.path.isdir(directory_path))


def run_check_command(container, check_item):
    for (function_name, argument) in check_item:
        container.attach_wait(function_name, argument)


def print_result_of_check_item(container_name, check_item):
    container = lxc.Container(container_name)
    print("Container name: %s" % container_name)

    container.start()
    run_check_command(container, check_item)
    shutdown_container(container)


def print_installation_result_of_zabbix_server(container_name):
    CHECK_ITEM = [[print_file_is_usable, "/usr/sbin/zabbix_server"],
                  [print_file_is_usable, "/usr/sbin/zabbix_agentd"]]

    print_result_of_check_item(container_name, CHECK_ITEM)


def print_installation_result_of_zabbix_agent(container_name):
    CHECK_ITEM = [[print_file_is_usable, "/usr/sbin/zabbix_agentd"]]

    print_result_of_check_item(container_name, CHECK_ITEM)


def print_installation_result_of_nagios_server3():
    CHECK_ITEM = [[print_file_is_usable, "/usr/sbin/nagios"],
                  [print_file_is_usable, "/usr/sbin/ndo2db"]]
    CONTAINER_NAME = "env_nagios_server3"

    print_result_of_check_item(CONTAINER_NAME, CHECK_ITEM)


def print_installation_result_of_nagios_server4():
    CHECK_ITEM = [[print_file_is_usable, "/usr/local/nagios/bin/nagios"],
                  [print_file_is_usable, "/usr/local/nagios/bin/ndo2db"]]
    CONTAINER_NAME = "env_nagios_server4"

    print_result_of_check_item(CONTAINER_NAME, CHECK_ITEM)


def print_installation_result_of_nagios_nrpe():
    CHECK_ITEM = [[print_file_is_usable, "/etc/nagios/nrpe.cfg"],
                  [print_directory_is_usable, "/usr/lib64/nagios/plugins/"]]
    CONTAINER_NAME = "env_nagios_nrpe"

    print_result_of_check_item(CONTAINER_NAME, CHECK_ITEM)


def print_installation_result_of_hatohol():
    CHECK_ITEM = [[print_file_is_usable, "/usr/sbin/hatohol"]]
    CONTAINER_NAME = "env_hatohol_rpm"

    print_result_of_check_item(CONTAINER_NAME, CHECK_ITEM)


def print_installation_result_of_redmine():
    CHECK_ITEM = [[print_directory_is_usable, "/var/lib/redmine"],
                  [print_file_is_usable, "/usr/local/bin/ruby"]]
    CONTAINER_NAME = "env_redmine"

    print_result_of_check_item(CONTAINER_NAME, CHECK_ITEM)


def print_installation_result_of_fluentd():
    CHECK_ITEM = [[print_file_is_usable, "/usr/sbin/td-agent"]]
    CONTAINER_NAME = "env_fluentd"

    print_result_of_check_item(CONTAINER_NAME, CHECK_ITEM)


def check_container_successfully():
    print_installation_result_of_hatohol()
    print_installation_result_of_zabbix_server("env_zabbix_server22")
    print_installation_result_of_zabbix_server("env_zabbix_server20")
    print_installation_result_of_zabbix_agent("env_zabbix_agent22")
    print_installation_result_of_zabbix_agent("env_zabbix_agent20")
    print_installation_result_of_nagios_server3()
    print_installation_result_of_nagios_server4()
    print_installation_result_of_nagios_nrpe()
    print_installation_result_of_redmine()
    print_installation_result_of_fluentd()


if __name__ == '__main__':
    if not os.geteuid() == 0:
        print("You need root permission to use this script.")
        sys.exit(1)

    if check_container_exist():
        check_container_successfully()
