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

def print_info(info_dict):
    print("%2s"%str(info_dict["id"] + 1) + " | " + "%-3s"%info_dict["group"] 
          + " | " + "%-12s"%container_name[info_dict["id"]] + " | " 
          + "%-12s"%info_dict["host"] + " | " + "%-12s"%info_dict["ip"] 
          + " | " + container_obj[info_dict["id"]].state + " | ")

def plug_frame(machine_id):
    if machine_id % 20 == 0 and machine_id != 0:
        print_frame()

def get_group_info(info_dict,machine_id):
    group_path = open("/var/lib/lxc/" + container_name[machine_id] + "/group")
    group_lines = group_path.readlines()
    group_path.close()

    info_dict["group"] = group_lines[0].rstrip()

def get_config_info(info_dict,machine_id):
    conf_path = open("/var/lib/lxc/" + container_name[machine_id] + "/config")
    conf_lines = conf_path.readlines()
    conf_path.close()
    
    for line in conf_lines:
        if line.find("lxc.network.ipv4 =") >= 0:
            line = line.split("=")
            line = line[1].split("/")
            info_dict["ip"] = line[0].lstrip()

        elif line.find("lxc.utsname =") >= 0:
            line = line.split("=")
            info_dict["host"] = line[1].rstrip()

def get_info_dict(machine_id):
    info_dict = {}
    get_config_info(info_dict,machine_id)
    get_group_info(info_dict,machine_id)
    info_dict["id"] = machine_id

    return info_dict

if __name__ == '__main__':
    print_frame()

    for machine_id in range(0,len(container_name)):
        plug_frame(machine_id)
        print_info(get_info_dict(machine_id))

