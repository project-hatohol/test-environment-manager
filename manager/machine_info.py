#! /usr/bin/env python3

import lxc
import sys
import os.path

container_list = lxc.list_containers()
container_obj_list = lxc.list_containers(as_object=True)

def print_template():
    print ("-----------------------------------------------------------------")
    print ("%-3s"%"No" + "|" + "%5s"%"Group" + "|" + "%15s"%"Name     |"
           + "%15s"%"HostName   |" + "%15s"%"IP      |" + "%10s"%"State  |")
    print ("-----------------------------------------------------------------")


def print_container_info(dict):
    print("%2s"%str(dict["id"] + 1) + " | " + "%-3s"%dict["group"] 
          + " | " + "%-12s"%container_list[dict["id"]] + " | " 
          + "%-12s"%dict["host"] + " | " + "%-12s"%dict["ip"] 
          + " | " + container_obj_list[dict["id"]].state + " | ")


def plug_template(count):
    punctuation = 20
    if count % punctuation == 0 and count != 0:
        print_template()


def get_group_info(info_dict, machine_id):
    group_file = open("/var/lib/lxc/" + container_list[machine_id] + "/group")
    group_lines = group_file.readlines()
    group_file.close()

    info_dict["group"] = group_lines[0].rstrip()


def get_config_info(info_dict, machine_id):
    conf_file = open("/var/lib/lxc/" + container_list[machine_id] + "/config")
    conf_lines = conf_file.readlines()
    conf_file.close()

    for line in conf_lines:
        if line.find("lxc.network.ipv4 =") >= 0:
            (key, address_and_mask) = line.split("=")
            (address, mask) = address_and_mask.split("/")
            info_dict["ip"] = address

        elif line.find("lxc.utsname =") >= 0:
            (key, host) = line.split("=")
            info_dict["host"] = host.rstrip()


def get_info_dict(machine_id):
    info_dict = {}
    get_config_info(info_dict, machine_id)
    get_group_info(info_dict, machine_id)
    info_dict["id"] = machine_id

    return info_dict


if __name__ == '__main__':
    print_template()

    for machine_id in range(len(container_list)):
        plug_template(machine_id)
        print_container_info(get_info_dict(machine_id))

