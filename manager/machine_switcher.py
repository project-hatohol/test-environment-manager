#! /usr/bin/env python3

import lxc
import sys
import os.path

con_name = lxc.list_containers()
con_obj = lxc.list_containers(as_object=True)

def switcher(machine_id) :
    if con_obj[machine_id].state == "STOPPED" :
            print(con_name[machine_id] + " | " + "Start "
                                +str(con_obj[machine_id].start()))
    if con_obj[machine_id].state == "RUNNING" :
        stdn = con_obj[machine_id].shutdown()
        print(con_name[machine_id] + " | " + "Shutdown "+str(stdn))
        if not stdn:
             print(con_name[machine_id] + " | " + "Stop "
                                +str(con_obj[machine_id].stop()))
def ArgSeparator() :
    lists = []
    for select in sys.argv[2:] :
        if "-" in select :
            hoge = select.split("-")
            for num in range(int(hoge[0]),int(hoge[1])+1) :
                lists.append(num)
        else :
            lists.append(int(select))
    return lists

def CreateGroupDict() :
    dict = {}

    machine_id = 0
    while machine_id < len(con_name) :
        ld = open("/var/lib/lxc/"+ con_name[machine_id] +"/group")
        gr_lines = ld.readlines()
        ld.close()
        group = int(gr_lines[0].rstrip())
        
        if group not in dict :
            dict[group] = [machine_id]
        else :
            dict[group].append(machine_id)   

        machine_id += 1

    return dict

if __name__ == '__main__' :
    arglist = ArgSeparator()
    
    if sys.argv[1] == "m" :
        for machine_id in arglist :
            switcher(machine_id-1)

    elif sys.argv[1] == "g" :
        groupdict = CreateGroupDict()
        for group in arglist :
            for machine_id in groupdict[group] :
                switcher(machine_id)

    else :
        print("You must input the first argument as 'm' or 'g'.")

