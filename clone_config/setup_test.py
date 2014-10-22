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

    return path_dict


def add_path_to_path_dict(setup_func_name, path_dict, container_name):
    if setup_func_name == "zabbix-agent":
        path_dict[container_name] = definevalue.ZBX_AGT_PATH
    elif setup_func_name == "zabbix-server":
        path_dict[container_name] = definevalue.ZBX_SRV_PATH
    elif setup_func_name == "nrpe":
        path_dict[container_name] = definevalue.NRPE_PATH
    elif setup_func_name == "redmine":
        path_dict[container_name] = definevalue.REDMINE_PATH
    elif setup_func_name == "fluentd":
        path_dict[container_name] = definevalue.TD_AGENT_PATH
    elif setup_func_name == "nagios3":
        path_dict[container_name] = definevalue.NAGIOS3_PATH
    elif setup_func_name == "nagios4":
        path_dict[container_name] = definevalue.NAGIOS4_PATH


def find_file(path):
    print(path + " : " + str(os.path.exists(path)))


def check_file_exists(container_name, path_dict):
    print("%s:" % container_name)
    container = lxc.Container(container_name)
    container.start()

    for path in path_dict[container_name].values():
        container.attach_wait(find_file, path)
    utils.shutdown_container(container)


if __name__ == '__main__':
    argvs = sys.argv
    utils.exit_if_user_run_this_as_general_user()
    utils.exit_if_argument_is_not_given(len(argvs))

    setting_dict = create_setting_dict(argvs[1])
    path_dict = create_path_dict(setting_dict)
    for container_name in path_dict.keys():
        check_file_exists(container_name, path_dict)
