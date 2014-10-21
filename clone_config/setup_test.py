#! /usr/bin/env python3

import sys
import os.path
import lxc
import traceback
import apport
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


def create_setting_dict(yaml_path):
    setting_dict = {}
    config_info = utils.get_config_info(yaml_path)

    for container_name in config_info.keys():
        for setup_element_key in config_info[container_name].keys():
            add_according_key(setting_dict, container_name, setup_element_key)

    return setting_dict


def create_path_dict(setting_dict):
    path_dict = {}
    for container_name in setting_dict.keys():
        for setup_func_name in setting_dict[container_name]:
            add_path_to_path_dict(setup_func_name, path_dict, container_name)

    for key in path_dict.keys():
        path_dict[key] = consolidate_path_type(path_dict[key])

    return path_dict


def add_path_to_path_dict(setup_func_name, path_dict, container_name):
    if setup_func_name == "zabbix-agent":
        path_dict[container_name] = definevalue.ZABBIX_CONF_FILE_PATH

    elif setup_func_name == "zabbix-server":
        path_dict[container_name] = [definevalue.ZABBIX_CONF_SERVER_PATH,
                          definevalue.ZABBIX_CONF_HTTPD_PATH,
                          definevalue.ZABBIX_CONF_PHP_PATH]
    elif setup_func_name == "nrpe":
        path_dict[container_name] = definevalue.NRPE_FILE_PATH

    elif setup_func_name == "redmine":
        path_dict[container_name] = definevalue.REDMINE_LIST_OF_PATH

    elif setup_func_name == "fluentd":
        path_dict[container_name] = definevalue.TD_AGENT_FILE_PATH

    elif setup_func_name == "nagios3":
        path_dict[container_name] = definevalue.NAGIOS3_LIST_OF_PATH

    elif setup_func_name == "nagios4":
        path_dict[container_name] = definevalue.NAGIOS4_LIST_OF_PATH


def consolidate_path_type(paths):
    path_list = []

    if isinstance(paths, str):
        path_list.append(paths)

    elif isinstance(paths, list):
        for path in paths:
            path_list.append(path)

    elif isinstance(paths, dict):
        for path in paths.values():
            path_list.append(path)

    return path_list


def find_file(path):
    print(path + " : " + str(os.path.exists(path)))


def execute_in_container(container_name, func_name, func_arg):
    container = lxc.Container(container_name)
    container.start()
    container.get_ips(timeout=definevalue.TIMEOUT_VALUE)

    container.attach_wait(find_file, func_arg)


if __name__ == '__main__':
    utils.exit_if_user_run_this_as_general_user()
    utils.exit_if_argument_is_not_given()

    setting_dict = create_setting_dict(sys.argv[1])
    path_dict = create_path_dict(setting_dict)
    for key in path_dict.keys():
        for path in path_dict[key]:
            execute_in_container(key, find_file, path)
