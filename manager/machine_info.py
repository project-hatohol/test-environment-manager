#! /usr/bin/env python3

import lxc
import sys
import os.path

def frame():
	print ("-------------------------------------------------------------------------")
	print ("%-3s"%"No"+"|"+"%5s"%"Group"+"|"+"%15s"%"Name     |"
           +"%15s"%"HostName   |"+"%15s"%"IP      |"+"%10s"%"State  |")
	print ("-------------------------------------------------------------------------")

con_name = lxc.list_containers()
con_obj = lxc.list_containers(as_object=True)
print ("\nMahcine list:\n")
frame()

machine_id = 0
while machine_id < len(con_name):
	ld = open("/var/lib/lxc/"+con_name[machine_id]+"/config")
	conf_lines = ld.readlines()
	ld.close()

	for line in conf_lines:
		if line.find("lxc.network.ipv4 =") >= 0:
			ip = line[19:-4]
		if line.find("lxc.utsname =") >= 0:
			host = line[14:-1]

	ld = open("/var/lib/lxc/"+con_name[machine_id]+"/group")
	gr_lines = ld.readlines()
	ld.close()

	group = gr_lines[0].rstrip()

	if machine_id%20 == 0 and machine_id != 0:
		frame()

	print("%2s"%str(machine_id + 1) + " | " + "%-3s"%group +" | "
          +"%-12s"%con_name[machine_id] + " | " +"%-12s"%host+" | "
          +"%-12s"%ip + " | " +con_obj[machine_id].state+" | ")

	machine_id += 1

