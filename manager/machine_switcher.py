#! /usr/bin/env python3

import lxc
import sys
import os.path

container_name = lxc.list_containers()
container_obj = lxc.list_containers(as_object=True)

def change_state(machine_id):
    if container_obj[machine_id].state == "STOPPED":
            print(container_name[machine_id] + " | " + "Start "
                  + str(container_obj[machine_id].start()))
    
    if container_obj[machine_id].state == "RUNNING":
        stdn = container_obj[machine_id].shutdown()
        print(container_name[machine_id] + " | " + "Shutdown " + str(stdn))
        if not stdn:
             print(container_name[machine_id] + " | " + "Stop "
                   + str(container_obj[machine_id].stop()))
def separate_arg():
    lists = []
    for select in sys.argv[2:]:
        if "-" in select:
            select = select.split("-")
            for num in range(int(seelct[0]),int(select[1]) + 1):
                lists.append(num)
        else:
            lists.append(int(select))
    return lists

def create_group_dict():
    dict = {}

    for machine_id in range(0,len(container_name)):
        group_path = open("/var/lib/lxc/" + container_name[machine_id] + "/group")
        group_lines = group_path.readlines()
        ld.close()
        group = int(group_lines[0].rstrip())
        
        if group not in dict:
            dict[group] = [machine_id]
        else:
            dict[group].append(machine_id)   

    return dict

if __name__ == '__main__':
    arg_list = separate_arg()
    
    if sys.argv[1] == "m":
        for machine_id in arg_list:
            change_state(machine_id - 1)

    elif sys.argv[1] == "g":
        group_dict = create_group_dict()
        for group in arg_list:
            for machine_id in group_dict[group]:
                change_state(machine_id)

    else:
        print("You must input the first argument as 'm' or 'g'.")

