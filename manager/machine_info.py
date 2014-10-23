#! /usr/bin/env python3

import lxc
import sys
import os.path


def print_header():
    print ('-----------------------------------------------------------------\n'
           + '%-3s'%'No' + '|' + '%5s'%'Group' + '%-15s'%'| Name'
           + '%-15s'%'| HostName' + '%-15s'%'| IP' + '%-7s'%'| State   |\n'
           '-----------------------------------------------------------------')


def print_container_info(dict, container_list, container_obj_list):
    print('%2s'%str(dict['id'] + 1) + ' | ' + '%-3s'%dict['group'] 
          + ' | ' + '%-12s'%container_list[dict['id']] + ' | ' 
          + '%-12s'%dict['host'] + ' | ' + '%-12s'%dict['ip'] 
          + ' | ' + container_obj_list[dict['id']].state + ' | ')


def read_file(container_path, file_name):
    file = open(container_path + file_name)
    lines = file.readlines()
    file.close()

    return lines


def get_container_path(container_name):
    container_path = '/var/lib/lxc/' + container_name + '/'

    return container_path


def get_id_info(info_dict, container_id):
    info_dict['id'] = container_id


def get_group_info(info_dict, container_path):
    if os.path.exists(container_path + "group"):
        info_dict["group"] = read_file(container_path, "group")[0].rstrip()
    else:
        info_dict["group"] = "N/A"

def get_config_info(info_dict, container_path):
    conf_lines = read_file(container_path, 'config')
    for line in conf_lines:
        if line.find("lxc.network.ipv4") >= 0:
            (key, address) = line.split("=")
            info_dict["ip"] = address.strip()

        elif line.find("lxc.utsname") >= 0:
            (key, host) = line.split("=")
            info_dict["host"] = host.strip()


def get_info_dict(container_id, container_path):
    info_dict = {}
    get_id_info(info_dict, container_id)
    get_config_info(info_dict, container_path)
    get_group_info(info_dict, container_path)

    return info_dict


if __name__ == '__main__':
    container_obj_list = lxc.list_containers(as_object=True)
    container_list = lxc.list_containers()

    print_header()
    for container_id in range(len(container_list)):
        container_path = get_container_path(container_list[container_id])
        print_container_info(get_info_dict(container_id, container_path),
                             container_list, container_obj_list)

