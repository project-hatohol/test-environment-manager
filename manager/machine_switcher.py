#! /usr/bin/env python3

import lxc
import sys
import os.path

def switcher(num) :
    if con_obj[num] == "STOPPED" :
            print(con_name[num] + " | " + "Start "
                                +str(con_obj[num].start()))
    else :
        stdn = con_obj[num].shutdown()
        print(con_name[lists[num] + " | " + "Shutdown "+str(stdn))
        if not stdn:
             print(con_name[num] + " | " + "Stop "
                                +str(con_obj[num].stop()))

for select in sys.argv[2:] :
    lists = []
    if "-" in select :
        select = int(num.split("-"))
        num = 0
        for range(int(select[0]),int(select[1])+1) :
            lists.append(int(select[0])+num)
            num+=1
    else :
        lists.append(int(select))

con_name = lxc.list_containers()
con_obj = lxc.list_containers(as_object=True)

if sys.argv[1] == "m" :
    num = 0
    while num < len(lists) :
        switcher(lists[num-1])    
        num += 1

else if sys.argv[1] == "g" :
    num = 0
    while num < len(con_name) :
        ld = open("/var/lib/lxc/"+con_obj[num]+"group")
        gr_lines = group.readlines()
        ld.close()
        group = int(gr_lines[0].rstrip())

        if group not in dict:
            dict = {group:None}
        dict[group].append(num)

        num += 1
    
    for num in lists :
        for num2 in dict[num]
            switcher(num2)

else
    print("You must input the first argument as 'm' or 'g'.")

