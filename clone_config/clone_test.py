#! /usr/bin/env python3

import lxc
import sys
import os
sys.path.append("../common")
import utils

def get_container_list(yaml_path):
    container_list = utils.get_config_info(yaml_path).keys()

    return container_list


def check_containers_ware_generated(container_list):
    all_container_list = lxc.list_containers()

    for container_name in container_list:
        if container_name in all_container_list:
            print(container_name + " was generated.")
        else:
            print(container_name + " was not generated.")


if __name__ == '__main__':
    sample_yaml_path = sys.argv[1]
    check_containers_ware_generated(get_container_list(sample_yaml_path))
