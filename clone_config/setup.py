#!/usr/bin/env python3
import os
import sys
import subprocess
import yaml
import lxc
sys.path.append("../common")
import definevalue
from utils import *
import clone

def prepare_setup_zabbix_server(argument):
    print("Not implemented yet: prepare_setup_zabbix_server")
    run_argument = []
    return run_argument


def run_setup_zabbix_server(argument):
    print("Not implemented yet: run_setup_zabbix_server")


def prepare_setup_zabbix_agent(argument):
    print("Not implemented yet: prepare_setup_zabbix_agent")
    run_argument = []
    return run_argument


def run_setup_zabbix_agent(argument):
    print("Not implemented yet: run_setup_zabbix_agent")


def prepare_setup_nagios_server3(argument):
    print("Not implemented yet: prepare_setup_nagios_server3")
    run_argument = []
    return run_argument


def run_setup_nagios_server3(argument):
    print("Not implemented yet: run_setup_nagios_server3")


def prepare_setup_nagios_server4(argument):
    print("Not implemented yet: prepare_setup_nagios_server4")
    run_argument = []
    return run_argument


def run_setup_nagios_server4(argument):
    print("Not implemented yet: run_setup_nagios_server4")


def prepare_setup_nagios_nrpe(argument):
    print("Not implemented yet: prepare_setup_nagios_nrpe")
    run_argument = []
    return run_argument


def run_setup_nagios_nrpe(argument):
    CONFIG_FILE_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/clone_config-settings/clone_config/assets/nrpe.cfg"
    NRPE_FILE_PATH = "/etc/nagios/nrpe.cfg"
    CMD = ["wget", "-P", "/etc/nagios/", CONFIG_FILE_URL]

    os.remove(NRPE_FILE_PATH)
    subprocess.call(CMD)


def prepare_setup_redmine(argument):
    print("Not implemented yet: prepare_setup_redmine")
    run_argument = []
    return run_argument


def run_setup_redmine(argument):
    print("Not implemented yet: run_setup_redmine")


def prepare_setup_fluentd(argument):
    print("Not implemented yet: prepare_setup_fluentd")
    run_argument = []
    return run_argument


def run_setup_fluentd(argument):
    CONFIG_FILE_URL = "https://raw.githubusercontent.com/project-hatohol/test-environment-manager/clone_config-settings/clone_config/assets/td-agent.conf"
    TD_AGENT_FILE_PATH = "/etc/td-agent/td-agent.conf"
    CMD = ["wget", "-P", "/etc/td-agent/", CONFIG_FILE_URL]

    os.remove(TD_AGENT_FILE_PATH)
    subprocess.call(CMD)


SETUP_FUNCTIONS = {"zabbix-server": run_setup_zabbix_server,
                   "zabbix-agent": run_setup_zabbix_agent,
                   "nagios3": run_setup_nagios_server3,
                   "nagios4": run_setup_nagios_server4,
                   "nrpe": run_setup_nagios_nrpe,
                   "redmine": run_setup_redmine,
                   "fluentd": run_setup_fluentd}

PREPARE_FUNCTIONS = {run_setup_zabbix_server: prepare_setup_zabbix_server,
                     run_setup_zabbix_agent: prepare_setup_zabbix_agent,
                     run_setup_nagios_server3: prepare_setup_nagios_server3,
                     run_setup_nagios_server4: prepare_setup_nagios_server4,
                     run_setup_nagios_nrpe: prepare_setup_nagios_nrpe,
                     run_setup_redmine: prepare_setup_redmine,
                     run_setup_fluentd: prepare_setup_fluentd}


def get_function_and_arguments(info_of_container_name, list_of_key_in_info):
    list_of_setup_function = SETUP_FUNCTIONS.keys()
    return_list = []
    for key_in_info in list_of_key_in_info:
        if not key_in_info in list_of_setup_function:
            continue
        else:
            info_of_function = info_of_container_name[key_in_info]
            function_argument = []
            if info_of_function is not None:
                function_argument.append(info_of_function)
            return_list.append([SETUP_FUNCTIONS[key_in_info], function_argument])

    return return_list


def get_container_name_and_function_to_setup(config_info_name):
    list_of_container_name = config_info_name.keys()
    return_list = []
    for container_name in list_of_container_name:
        info_of_container_name = config_info_name[container_name]
        list_of_key_in_info = info_of_container_name.keys()
        setup_functions = get_function_and_arguments(info_of_container_name,
                                                     list_of_key_in_info)
        return_list.append([container_name, setup_functions])

    return return_list


def setup_container(container_name, run_function_names):
    print("Start setup process: %s" % container_name)
    container = lxc.Container(container_name)
    container.start()
    container.get_ips(timeout=definevalue.TIMEOUT_VALUE)

    for (run_function_name, argument) in run_function_names:
        run_argument = PREPARE_FUNCTIONS[run_function_name](argument)
        container.attach_wait(run_function_name, run_argument)

    shutdown_container(container)


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
