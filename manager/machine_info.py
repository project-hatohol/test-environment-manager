#! /usr/bin/env python3

import lxc
import sys
import os.path

con_name = lxc.list_containers()
con_obj = lxc.list_containers(as_object=True)

def Frame(machine_id):
    print ("-----------------------------------------------------------------")
    print ("%-3s"%"No"+"|"+"%5s"%"Group"+"|"+"%15s"%"Name     |"
           +"%15s"%"HostName   |"+"%15s"%"IP      |"+"%10s"%"State  |")
    print ("-----------------------------------------------------------------")

def PrintInfo(InfoDict) :
    print("%2s"%str(InfoDict["id"]+1) + " | " + "%-3s"%InfoDict["group"] +" | "
          +"%-12s"%con_name[InfoDict["id"]] + " | " +"%-12s"%InfoDict["host"]+" | "
          +"%-12s"%InfoDict["ip"] + " | " +con_obj[InfoDict["id"]].state+" | ")

def GetInfoDict(machine_id) :
    InfoDict = {}
    ld = open("/var/lib/lxc/"+con_name[machine_id]+"/config")
    conf_lines = ld.readlines()
    ld.close()
    
    for line in conf_lines:
        if line.find("lxc.network.ipv4 =") >= 0:
            InfoDict["ip"] = line[19:-4]
        if line.find("lxc.utsname =") >= 0:
            InfoDict["host"] = line[14:-1]

    ld = open("/var/lib/lxc/"+con_name[machine_id]+"/group")
    gr_lines = ld.readlines()
    ld.close()

    InfoDict["group"] = gr_lines[0].rstrip()
    InfoDict["id"] = machine_id

    return InfoDict

if __name__ == '__main__' :
    Frame()

    machine_id = 0
    while machine_id < len(con_name):
        if machine_id%20 == 0 and machine_id != 0:
            Frame()

        PrintInfo(GetInfoDict(machine_id))

        machine_id += 1

