#! /usr/bin/env python3

import lxc
import sys
import os.path

container_name = lxc.list_containers()
container_obj = lxc.list_containers(as_object=True)

def print_frame():
    print ("-----------------------------------------------------------------")
    print ("%-3s"%"No" + "|" + "%5s"%"Group" + "|" + "%15s"%"Name     |"
           + "%15s"%"HostName   |" + "%15s"%"IP      |" + "%10s"%"State  |")
    print ("-----------------------------------------------------------------")

def print_info(dict):
    print("%2s"%str(dict["id"] + 1) + " | " + "%-3s"%dict["group"] 
          + " | " + "%-12s"%container_name[dict["id"]] + " | " 
          + "%-12s"%dict["host"] + " | " + "%-12s"%dict["ip"] 
          + " | " + container_obj[dict["id"]].state + " | ")

def plug_frame(count):
    if count % 20 == 0 and count != 0:
        print_frame()

def get_group_info(info_dict, machine_id):
    group_file = open("/var/lib/lxc/" + container_name[machine_id] + "/group")
    group_lines = group_file.readlines()
    group_file.close()

    info_dict["group"] = group_lines[0].rstrip()

def get_config_info(info_dict, machine_id):
    conf_file = open("/var/lib/lxc/" + container_name[machine_id] + "/config")
    conf_lines = conf_file.readlines()
    conf_file.close()

    for line in conf_lines:
        if line.find("lxc.network.ipv4 =") >= 0:
            (trash,address_and_mask) = line.split("=")
            (address,mask) = address_and_mask.split("/")
            info_dict["ip"] = address

        elif line.find("lxc.utsname =") >= 0:
            (trash,host) = line.split("=")
            info_dict["host"] = host.rstrip()

def get_info_dict(machine_id):
    info_dict = {}
    get_config_info(info_dict,machine_id)
    get_group_info(info_dict,machine_id)
    info_dict["id"] = machine_id

    return info_dict

if __name__ == '__main__':
    print_frame()

    container_list_len = len(container_name)
    for machine_id in range(container_list_len):
        plug_frame(machine_id)
        print_info(get_info_dict(machine_id))

