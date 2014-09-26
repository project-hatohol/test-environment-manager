#! /usr/bin/env python3

import lxc
import sys
import os.path

container_list = lxc.list_containers()
container_obj_list = lxc.list_containers(as_object=True)

def toggle_state(machine_id):
    obj = container_obj_list[machine_id]
    name = container_list[machine_id]
    if obj.state == "STOPPED":
        start_state(machine_id, obj, name)
    else:
        stop_state(machine_id, obj, name)

def start_state(machine_id, obj, name):
    start_result = str(obj.start())
    print(name + " | " + "Start " + start_result)


def stop_state(machine_id, obj, name):
    succeed_shutdown = obj.shutdown()
    print(name + " | " + "Shutdown " + str(succeed_shutdown))
    if not succeed_shutdown:
        stop = obj.stop()
        print(name + " | " + "Stop " + str(stop))


def toggle_state_for_group(group_id_list):
    group_dict = create_group_dict()
    for group_id in group_id_list:
        toglle_each_machine_state(group_dict[group_id])


def toggle_each_machine_state(machine_id_list):
    for machine_id in machine_id_list:
        toggle_state(machine_id)


def convert_machine_nums_to_ids(machine_num_list):
    machine_id_list = [int(machine_num) - 1 for machine_num in machine_num_list]    

    return machine_id__list


def separate_id_list():
    lists = []
    select_arg = 2
    for select_id in sys.argv[select_arg:]:
        if "-" in select_id:
            (min, max) = select_id.split("-")
            for id in range(min, max+1):
                lists.append(id)
        else:
            lists.append(int(select_id))
    return lists


def create_group_dict():
    dict = {}
    container_list_len = len(container_list)
    for machine_id in range(container_list_len):
        group_file = open("/var/lib/lxc/" + container_list[machine_id] + "/group")
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
        toggle_each_machine_state(machine_id_list)

    elif sys.argv[1] == "g":
        group_id_list = separate_id_list()
        toggle_state_for_group(group_id_list)

    else:
        print("You must input the first argument as 'm' or 'g'.")

