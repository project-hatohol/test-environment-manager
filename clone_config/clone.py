#!/usr/bin/env python3
import os
import sys
import yaml
import lxc
import utils

NAME_BASE_CONTAINER = "base_container"

def get_config_info_from_yaml_file(file_path):
    yaml_file = open(file_path).read()
    return yaml.load(yaml_file)


def get_container_name_and_base_container_name(config_info_name):
    list_of_container_name = config_info_name.keys()
    return_list = []
    for container_name in list_of_container_name:
        if not NAME_BASE_CONTAINER in config_info_name[container_name]:
            continue
        else:
            return_list.append([container_name,
                                config_info_name[container_name]
                                [NAME_BASE_CONTAINER]])

    return return_list


if __name__ == '__main__':
    argvs = sys.argv
    utils.finish_if_user_run_as_general_user()
    utils.finish_if_argument_is_not_given(len(argvs))
