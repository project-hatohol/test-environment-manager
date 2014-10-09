#!/usr/bin/env python3
import os
import sys
import yaml
import lxc
sys.path.append("../common")
import definevalue
from utils import *
import clone

def run_setup_zabbix_server():
    print("Not implemented yet: run_setup_zabbix_server")


def run_setup_zabbix_agent():
    print("Not implemented yet: run_setup_zabbix_agent")


def run_setup_nagios_server3():
    print("Not implemented yet: run_setup_nagios_server3")


def run_setup_nagios_server4():
    print("Not implemented yet: run_setup_nagios_server4")


def run_setup_nagios_nrpe():
    print("Not implemented yet: run_setup_nagios_nrpe")


def run_setup_redmine():
    print("Not implemented yet: run_setup_redmine")


def run_setup_fluentd():
    print("Not implemented yet: run_setup_fluentd")


SETUP_FUNCTIONS = {"zabbix-server": run_setup_zabbix_server,
                   "zabbix-agent": run_setup_zabbix_agent,
                   "nagios3": run_setup_nagios_server3,
                   "nagios4": run_setup_nagios_server4,
                   "nrpe": run_setup_nagios_nrpe,
                   "redmine": run_setup_redmine,
                   "fluentd": run_setup_fluentd}

# TODO: Add a parameter for setup function as a part of sequence.
def get_container_name_and_function_to_setup(config_info_name):
    list_of_container_name = config_info_name.keys()
    list_of_setup_function = SETUP_FUNCTIONS.keys()
    return_list = []
    for container_name in list_of_container_name:
        info_of_container_name = config_info_name[container_name]
        list_of_key_in_info = info_of_container_name.keys()
        setup_functions = []
        for key_in_info in list_of_key_in_info:
            if not key_in_info in list_of_setup_function:
                continue
            else:
                setup_functions.append(key_in_info)
            return_list.append([container_name, setup_functions])

    return return_list


def setup_container(container_name, run_function_name):
    container = lxc.Container(container_name)
    container.start()
    container.get_ips(timeout=definevalue.TIMEOUT_VALUE)

    container.attach_wait(run_function_name)


def setup_containers(list_of_setup_containers):
    for (container_name, setup_function) in list_of_setup_containers:
        setup_container(container_name, setup_function)


def start_setup(yaml_file_path):
    config_info = clone.get_config_info(yaml_file_path)
    list_of_setup_containers = \
        get_container_name_and_function_to_setup(config_info)
    setup_containers(list_of_setup_containers)


if __name__ == '__main__':
    argvs = sys.argv
    exit_if_user_run_this_as_general_user()
    exit_if_argument_is_not_given(len(argvs))

    start_setup(argvs[1])
