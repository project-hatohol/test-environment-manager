#! /usr/bin/env python3

import lxc
import sys
import os.path

container_list = lxc.list_containers()
container_obj_list = lxc.list_containers(as_object=True)

def print_header():
    print ("-----------------------------------------------------------------\n"
           + "%-3s"%"No" + "|" + "%5s"%"Group" + "%-15s"%"| Name"
           + "%-15s"%"| HostName" + "%-15s"%"| IP" + "%-7s"%"| State   |\n"
           "-----------------------------------------------------------------")


def print_container_info(dict):
    print("%2s"%str(dict["id"] + 1) + " | " + "%-3s"%dict["group"] 
          + " | " + "%-12s"%container_list[dict["id"]] + " | " 
          + "%-12s"%dict["host"] + " | " + "%-12s"%dict["ip"] 
          + " | " + container_obj_list[dict["id"]].state + " | ")


def insert_header(line_number):
    punctuation = 20
    if line_number % punctuation == 0:
        print_header()


def read_file(container_name, file_name):
    file = open("/var/lib/lxc/" + container_name + "/" + file_name)
    lines = file.readlines()
    file.close()

    return lines


def get_container_name(machine_id):
    container_name = container_list[machine_id]
    return container_name


def get_group_info(info_dict, container_name):
    info_dict["group"] = read_file(container_name, "group")[0].rstrip()


def get_config_info(info_dict, container_name):
    conf_lines = read_file(container_name, "config")
    for line in conf_lines:
        if line.find("lxc.network.ipv4") >= 0 and line.find("/") >= 0:
            (key, address_and_mask) = line.split("=")
            (address, mask) = address_and_mask.split("/")
            info_dict["ip"] = address.lstrip()

        elif line.find("lxc.utsname") >= 0:
            (key, host) = line.split("=")
            info_dict["host"] = host.strip()


def get_info_dict(machine_id):
    info_dict = {}
    container_name = get_container_name(machine_id)
    get_config_info(info_dict, container_name)
    get_group_info(info_dict, container_name)
    info_dict["id"] = machine_id

    return info_dict


if __name__ == '__main__':
    for machine_id in range(len(container_list)):
        insert_header(machine_id)
        print_container_info(get_info_dict(machine_id))

