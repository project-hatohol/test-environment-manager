#!/usr/bin/env python3
import os
import os.path
import sys
import lxc
sys.path.append("../common")
import definevalue
from utils import *

def check_and_print_if_container_exists(container_name):
    result = lxc.Container(container_name).defined
    print("\"%s\" container exists: %r" % (container_name, result))

    return result


def list_containers_and_abort_if_one_does_not_exist(containers):
    for container_name in containers:
        result = check_and_print_if_container_exists(container_name)
        if not result:
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


def print_installation_result():
    ARGS = [["env_zabbix_server22",
             ["/usr/sbin/zabbix_server", "/usr/sbin/zabbix_agentd"]],
            ["env_zabbix_server20",
             ["/usr/sbin/zabbix_server", "/usr/sbin/zabbix_agentd"]],
            ["env_zabbix_agent22",
             ["/usr/sbin/zabbix_agentd"]],
            ["env_zabbix_agent20",
             ["/usr/sbin/zabbix_agentd"]],
            ["env_nagios_server3",
             ["/usr/sbin/nagios", "/usr/sbin/ndo2db"]],
            ["env_nagios_server4",
             ["/usr/local/nagios/bin/nagios", "/usr/local/nagios/bin/ndo2db"]],
            ["env_nagios_nrpe",
             ["/etc/nagios/nrpe.cfg", "/usr/lib64/nagios/plugins/"]],
            ["env_hatohol_rpm",
             ["/usr/sbin/hatohol"]],
            ["env_redmine",
             ["/var/lib/redmine", "/usr/local/bin/ruby"]],
            ["env_fluentd",
             ["/usr/sbin/td-agent"]]]

    for (container_name, list_of_path_to_check) in ARGS:
        print_result_of_check_item(container_name, list_of_path_to_check)


if __name__ == '__main__':
    finish_if_user_run_as_general_user()

    if list_containers_and_abort_if_one_does_not_exist(definevalue.CONTAINER_NAMES):
        print_installation_result()
