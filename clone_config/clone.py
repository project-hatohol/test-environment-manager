#!/usr/bin/env python3
import os
import sys
import yaml
import lxc

NAME_BASE_CONTAINER = "base_container"

def get_dictionary_from_yaml_file(file_path):
    yaml_file = open(file_path).read()
    return yaml.load(yaml_file)


def get_container_name_and_base_container(dictionary_name):
    list_of_container_name = dictionary_name.keys()
    return_list = []
    for container_name in list_of_container_name:
        if not NAME_BASE_CONTAINER in dictionary_name[container_name]:
            continue
        else:
            return_list.append([container_name,
                                dictionary_name[container_name]
                                [NAME_BASE_CONTAINER]])

    return return_list


if __name__ == '__main__':
    if not os.geteuid() == 0:
        print("You need root permission to use this script.")
        sys.exit(1)
