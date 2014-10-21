#!/usr/bin/env python3
import os
import sys
import yaml
import lxc
sys.path.append("../common")
import definevalue
from utils import *

def get_container_name_and_base_container_name(config_info):
    list_of_container_name = config_info.keys()
    return_list = []
    for container_name in list_of_container_name:
        key_of_base_name = definevalue.KEY_OF_BASE_CONTAINER
        key_of_container_name = config_info[container_name]
        if not key_of_base_name in key_of_container_name:
            continue
        else:
            return_list.append([container_name,
                                key_of_container_name[key_of_base_name]])

    return return_list


def clone_container(container_name, base_container_name):
    base_container = lxc.Container(base_container_name)
    container = base_container.clone(container_name, bdevtype="aufs",
                                     flags=lxc.LXC_CLONE_SNAPSHOT)
    return container.defined


def clone_containers(list_for_clone_container):
    for (container_name, base_container_name) in list_for_clone_container:
        if not lxc.Container(base_container_name).defined:
            print("Base container \"%s\" does not exist" % base_container_name)
            continue
        if lxc.Container(container_name).defined:
            print("\"%s\" already exists" % container_name)
            continue
        else:
            result = clone_container(container_name, base_container_name)
            print("Result of \"%s\": %r" % (container_name, result))


def start_clone_containers(yaml_file_path):
    config_info = get_config_info(yaml_file_path)
    list_of_clone_containers = \
        get_container_name_and_base_container_name(config_info)
    clone_containers(list_of_clone_containers)

    print("Finish clone container process!\n")


if __name__ == '__main__':
    argvs = sys.argv
    exit_if_user_run_this_as_general_user()
    exit_if_argument_is_not_given(len(argvs))

    start_clone_containers(argvs[1])
