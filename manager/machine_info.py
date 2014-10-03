#! /usr/bin/env python3

import lxc
import sys
import os.path


def print_header():
    print ("-----------------------------------------------------------------\n"
           + "%-3s"%"No" + "|" + "%5s"%"Group" + "%-15s"%"| Name"
           + "%-15s"%"| HostName" + "%-15s"%"| IP" + "%-7s"%"| State   |\n"
           "-----------------------------------------------------------------")


def print_container_info(dict, container_list, container_obj_list):
    print("%2s"%str(dict["id"] + 1) + " | " + "%-3s"%dict["group"] 
          + " | " + "%-12s"%container_list[dict["id"]] + " | " 
          + "%-12s"%dict["host"] + " | " + "%-12s"%dict["ip"] 
          + " | " + container_obj_list[dict["id"]].state + " | ")


def insert_header(exe_count):
    punctuation = 20
    if exe_count % punctuation == 0:
        print_header()


def read_file(container_path, file_name):
    file = open(container_path + file_name)
    lines = file.readlines()
    file.close()

    return lines


def get_container_path(container_name):
    container_path = "/var/lib/lxc/" + container_name + "/"

    return container_path


def get_id_info(info_dict, machine_id):
    info_dict["id"] = machine_id


def get_group_info(info_dict, container_path):
    info_dict["group"] = read_file(container_path, "group")[0].rstrip()


def get_config_info(info_dict, container_path):
    conf_lines = read_file(container_path, "config")
    for line in conf_lines:
        if line.find("lxc.network.ipv4") >= 0 and line.find("/") >= 0:
            (key, address_and_mask) = line.split("=")
            (address, mask) = address_and_mask.split("/")
            info_dict["ip"] = address.lstrip()

        elif line.find("lxc.utsname") >= 0:
            (key, host) = line.split("=")
            info_dict["host"] = host.strip()


def get_info_dict(machine_id, container_path):
    info_dict = {}
    get_id_info(info_dict, machine_id)
    get_config_info(info_dict, container_path)
    get_group_info(info_dict, container_path)

    return info_dict


if __name__ == '__main__':
    container_obj_list = lxc.list_containers(as_object=True)
    container_list = lxc.list_containers()

    for exe_count in range(len(container_list)):
        container_path = get_container_path(container_list[exe_count])
        insert_header(exe_count)
        print_container_info(get_info_dict(exe_count, container_path),
                             container_list, container_obj_list)

