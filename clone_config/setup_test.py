#! /usr/bin/env python3
import sys
import os.path
import lxc
import traceback
import apport
import subprocess
import time
sys.path.append("../common")
import utils
import definevalue

def add_according_key(setting_dict, container_name, setup_element_key):
    setup_functions = ["zabbix-server", "zabbix-agent", "nagios3",
                       "nagios4", "nrpe", "redmine", "fluentd"]

    if setup_element_key in setup_functions:
        if container_name in setting_dict:
            setting_dict[container_name].append(setup_element_key)
        else:
            setting_dict[container_name] = [setup_element_key]


def create_setting_dict(config_info):
    setting_dict = {}
    for container_name in config_info.keys():
        for setup_element_key in config_info[container_name].keys():
            add_according_key(setting_dict, container_name, setup_element_key)

    return setting_dict


def create_path_dict(setting_dict):
    path_dict = {}
    for container_name in setting_dict.keys():
        for setup_func_name in setting_dict[container_name]:
            add_path_to_path_dict(setup_func_name, path_dict, container_name)

    return path_dict


def add_path_to_path_dict(setup_func_name, path_dict, container_name):
    if setup_func_name in "zabbix-agent":
        path_dict[container_name] = definevalue.ZBX_AGT_PATH
    elif setup_func_name in "zabbix-server":
        path_dict[container_name] = definevalue.ZBX_SRV_PATH
    elif setup_func_name in "nrpe":
        path_dict[container_name] = definevalue.NRPE_PATH
    elif setup_func_name in "redmine":
        path_dict[container_name] = definevalue.REDMINE_PATH
    elif setup_func_name in "fluentd":
        path_dict[container_name] = definevalue.TD_AGENT_PATH
    elif setup_func_name in "nagios3":
        path_dict[container_name] = definevalue.NAGIOS3_PATH
    elif setup_func_name in "nagios4":
        path_dict[container_name] = definevalue.NAGIOS4_PATH


def add_process_name_to_path_dict(setup_func_name, process_dict, container_name):
    if setup_func_name in "zabbix-agent":
        process_dict[container_name] = ["zabbix_agentd"]
    elif setup_func_name in "zabbix-server":
        process_dict[container_name] = ["httpd", "zabbix_server", "zabbix_agentd"]
    elif setup_func_name in "nrpe":
        process_dict[container_name] = ["nrpe"]
    elif setup_func_name in "redmine":
        process_dict[container_name] = ["Passenger"]
    elif setup_func_name in "fluentd":
        process_dict[container_name] = ["td-agent"]
    elif setup_func_name in "nagios3":
        process_dict[container_name] = ["httpd", "nagios", "ndo2db"]
    elif setup_func_name in "nagios4":
        process_dict[container_name] = ["httpd", "nagios", "ndo2db"]


def create_process_dict(setting_dict):
    process_dict = {}
    for container_name in setting_dict.keys():
        for setup_func_name in setting_dict[container_name]:
            add_process_name_to_path_dict(setup_func_name, process_dict,
                                          container_name)

    return process_dict


def create_zabbix_hosts_dict(config_info):
    hosts_dict = {}
    for container_name in config_info.keys():
        if "zabbix-server" in config_info[container_name].keys():
            hosts_dict[container_name] =\
                config_info[container_name]["zabbix-server"]["target"]

    return hosts_dict


def find_file(path):
    print(path + " : " + str(os.path.exists(path)))


def find_process(process_names):
    # If this value isn't provided, find_process function shows processes
    # when init process is running.
    time.sleep(40)

    with subprocess.Popen(["ps", "ax"],
                          stdout=subprocess.PIPE,
                          universal_newlines=True) as proc:
        output = proc.stdout.read()
        for process_name in process_names:
            result = process_name in output
            print("Process %s: %r" % (process_name, result))


def check_file_exists(container_name, path_dict):
    print("%s:" % container_name)
    container = lxc.Container(container_name)
    container.start()

    for path in path_dict[container_name].values():
        container.attach_wait(find_file, path)
    utils.shutdown_container(container)


def check_process_exists(container_name, process_dict):
    print("%s:" % container_name)
    container = lxc.Container(container_name)
    container.start()
    container.attach_wait(find_process, process_dict[container_name])

    utils.shutdown_container(container)


if __name__ == '__main__':
    argvs = sys.argv
    utils.exit_if_user_run_this_as_general_user()
    utils.exit_if_argument_is_not_given(len(argvs))

    config_info = utils.get_config_info(argvs[1])
    setting_dict = create_setting_dict(config_info)
    path_dict = create_path_dict(setting_dict)
    process_dict = create_process_dict(setting_dict)
    zabbix_hosts_dict = create_zabbix_hosts_dict(config_info)
    for container_name in setting_dict.keys():
        check_file_exists(container_name, path_dict)
        check_process_exists(container_name, process_dict)
