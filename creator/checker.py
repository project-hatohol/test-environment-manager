#!/usr/bin/env python3
import lxc
import os
import sys
import os.path
import definevalue
from utils import *

def is_container_existed(container):
    if lxc.Container(definevalue.containers_name[container]).defined:
        print_container_exist_message(definevalue.containers_name[container])
        return True
    else:
        print_container_non_exist_message(definevalue.containers_name[container])
        return False


def check_container_exist():
    NAMES = ["base", "zabbix_server22", "zabbix_server20", "zabbix_agent22",
             "zabbix_agent20", "nagios_server3", "nagios_server4",
             "nagios_nrpe", "hatohol_build", "hatohol_rpm", "fluentd",
             "redmine"]

    for arg in NAMES:
        if not is_container_existed(arg):
            return False

    print_new_line()
    return True


def is_file_usable(file_path):
    if os.path.isfile(file_path):
        print("\"%s\" file exists: True" % file_path)
    else:
        print("\"%s\" file exists: False" % file_path)


def is_directory_usable(directory_path):
    if os.path.isdir(directory_path):
        print("\"%s\" directory exists: True" % directory_path)
    else:
        print("\"%s\" directory exists: False" % directory_path)


def define_container(container_key):
    container_name = definevalue.containers_name[container_key]
    print_container_name(container_name)

    return lxc.Container(container_name)


def check_zabbix_server_container(container_key):
    container = define_container(container_key)
    container.start()
    container.attach_wait(is_file_usable, "/usr/sbin/zabbix_server")
    container.attach_wait(is_file_usable, "/usr/sbin/zabbix_agentd")

    shutdown_container(container)
    print_new_line()


def check_zabbix_agent_container(container_key):
    container = define_container(container_key)
    container.start()
    container.attach_wait(is_file_usable, "/usr/sbin/zabbix_agentd")

    shutdown_container(container)
    print_new_line()


def check_nagios_server3_container():
    container_key = "nagios_server3"
    container = define_container(container_key)
    container.start()
    container.attach_wait(is_file_usable, "/usr/sbin/nagios")
    container.attach_wait(is_file_usable, "/usr/sbin/ndo2db")

    shutdown_container(container)
    print_new_line()


def check_nagios_server4_container():
    container_key = "nagios_server4"
    container = define_container(container_key)
    container.start()
    container.attach_wait(is_file_usable, "/usr/local/nagios/bin/nagios")
    container.attach_wait(is_file_usable, "/usr/local/nagios/bin/ndo2db")

    shutdown_container(container)
    print_new_line()


def check_nagios_nrpe_container():
    container_key = "nagios_nrpe"
    container = define_container(container_key)
    container.start()
    container.attach_wait(is_file_usable, "/etc/nagios/nrpe.cfg")
    container.attach_wait(is_directory_usable, "/usr/lib64/nagios/plugins/")

    shutdown_container(container)
    print_new_line()


def check_hatohol_container():
    container_key = "hatohol_rpm"
    container = define_container(container_key)
    container.start()
    container.attach_wait(is_file_usable, "/usr/sbin/hatohol")

    shutdown_container(container)
    print_new_line()


def check_redmine_container():
    container_key = "redmine"
    container = define_container(container_key)
    container.start()
    container.attach_wait(is_directory_usable, "/var/lib/redmine")
    container.attach_wait(is_file_usable, "/usr/local/bin/ruby")

    shutdown_container(container)
    print_new_line()


def check_fluentd_container():
    container_key = "fluentd"
    container = define_container(container_key)
    container.start()
    container.attach_wait(is_file_usable, "/usr/sbin/td-agent")

    shutdown_container(container)
    print_new_line()


def check_container_successfully():
    check_hatohol_container()
    check_zabbix_server_container("zabbix_server22")
    check_zabbix_server_container("zabbix_server20")
    check_zabbix_agent_container("zabbix_agent22")
    check_zabbix_agent_container("zabbix_agent20")
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
