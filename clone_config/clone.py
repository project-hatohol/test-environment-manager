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


def clone_container(container_name, base_container_name):
    base_container = lxc.Container(base_container_name)
    return base_container.clone(container_name, bdevtype="aufs",
                                flags=lxc.LXC_CLONE_SNAPSHOT)


def clone_containers_from(list_for_clone_container):
    for (container_name, base_container_name) in list_for_clone_container:
        if lxc.Container(container_name).defined:
            print("\"%s\" already exists" % container_name)
            continue
        else:
            result = clone_container(container_name, base_container_name)
            print("Result of \"%s\": %r" % (container_name, result))


if __name__ == '__main__':
    argvs = sys.argv
    utils.finish_if_user_run_as_general_user()
    utils.finish_if_argument_is_not_given(len(argvs))
