#!/usr/bin/env python3
import lxc
import os
import sys
import os.path
import definevalue
from utils import *

def print_container_is_existing():
    for container_name in definevalue.CONTAINER_NAME:
        if lxc.Container(container_name).defined:
            print("Container \"%s\": True" % container_name)
        else:
            print("Container \"%s\": False" % container_name)
            return False

    print_new_line()
    return True


def print_usability_of(file_path):
    print("\"%s\" exists: %r" % (file_path, os.path.exists(file_path)))


def run_check_command(container, list_of_path):
    for path in list_of_path:
        container.attach_wait(print_usability_of, path)


def print_result_of_check_item(container_name, list_of_path):
    container = lxc.Container(container_name)
    print("Container name: %s" % container_name)

    container.start()
    run_check_command(container, list_of_path)
    shutdown_container(container)


def print_installation_result_of_zabbix_server(container_name):
    LIST_OF_PATH = ["/usr/sbin/zabbix_server", "/usr/sbin/zabbix_agentd"]

    print_result_of_check_item(container_name, LIST_OF_PATH)


def print_installation_result_of_zabbix_agent(container_name):
    LIST_OF_PATH = ["/usr/sbin/zabbix_agentd"]

    print_result_of_check_item(container_name, LIST_OF_PATH)


def print_installation_result_of_nagios_server3():
    LIST_OF_PATH = ["/usr/sbin/nagios", "/usr/sbin/ndo2db"]
    CONTAINER_NAME = "env_nagios_server3"

    print_result_of_check_item(CONTAINER_NAME, LIST_OF_PATH)


def print_installation_result_of_nagios_server4():
    LIST_OF_PATH = ["/usr/local/nagios/bin/nagios",
                  "/usr/local/nagios/bin/ndo2db"]
    CONTAINER_NAME = "env_nagios_server4"

    print_result_of_check_item(CONTAINER_NAME, LIST_OF_PATH)


def print_installation_result_of_nagios_nrpe():
    LIST_OF_PATH = ["/etc/nagios/nrpe.cfg", "/usr/lib64/nagios/plugins/"]
    CONTAINER_NAME = "env_nagios_nrpe"

    print_result_of_check_item(CONTAINER_NAME, LIST_OF_PATH)


def print_installation_result_of_hatohol():
    LIST_OF_PATH = ["/usr/sbin/hatohol"]
    CONTAINER_NAME = "env_hatohol_rpm"

    print_result_of_check_item(CONTAINER_NAME, LIST_OF_PATH)


def print_installation_result_of_redmine():
    LIST_OF_PATH = ["/var/lib/redmine", "/usr/local/bin/ruby"]
    CONTAINER_NAME = "env_redmine"

    print_result_of_check_item(CONTAINER_NAME, LIST_OF_PATH)


def print_installation_result_of_fluentd():
    LIST_OF_PATH = ["/usr/sbin/td-agent"]
    CONTAINER_NAME = "env_fluentd"

    print_result_of_check_item(CONTAINER_NAME, LIST_OF_PATH)


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

    if print_container_is_existing():
        check_container_successfully()
