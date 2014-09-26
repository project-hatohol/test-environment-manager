#! /usr/bin/env python3

import lxc
import sys
import os.path

container_name = lxc.list_containers()
container_obj = lxc.list_containers(as_object=True)

def change_state(machine_id):
    obj = container_obj[machine_id]
    name = container_name[machine_id]
    if obj.state == "STOPPED":
            start_result = str(obj.start())
            print(name + " | " + "Start " + start_result)
    else:
        succeed_shutdown = obj.shutdown()
        print(name + " | " + "Shutdown " + str(succed_shutdown))
        if not succeed_shutdown:
             stop = obj.stop()
             print(name + " | " + "Stop " + str(stop))


def change_group_state(group_id_list):
    group_dict = create_group_dict()
    for group_id in group_id_list:
        change_machine_state(group_dict[group_id])


def change_machine_state(machine_id_list):
    for machine_id in machine_id_list:
        change_state(machine_id)


def convert_machine_num_to_id(machine_num_list):
    machine_id_list = [int(machine_num) - 1 for machine_num in machine_num_list]    

    return machine_id__list


def separate_id_list():
    lists = []
    for select_id in sys.argv[2:]:
        if "-" in select_id:
            max_min = select_id.split("-")
            max = max_min[1]
            min = max_min[0]
            for id in range(min, max+1):
                lists.append(id)
        else:
            lists.append(int(select_id))
    return lists


def create_group_dict():
    dict = {}
    container_list_len = len(container_name)
    for machine_id in range(container_list_len):
        group_file = open("/var/lib/lxc/" + container_name[machine_id] + "/group")
        group_lines = group_file.readlines()
        group_file.close()
        group_id = int(group_lines[0].rstrip())
        
        if group_id not in dict:
            dict[group_id] = [machine_id]
        else:
            dict[group_id].append(machine_id)   

    return dict


if __name__ == '__main__':
    if sys.argv[1] == "m":   
        machine_num_list = separate_id_list()
        machine_id_list = convert_machine_num_to_id(machine_num_list)
        change_machine_state(machine_id_list)

    elif sys.argv[1] == "g":
        group_id_list = separate_id_list()
        change_group_state(group_id_list)

    else:
        print("You must input the first argument as 'm' or 'g'.")

