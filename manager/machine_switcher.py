#st_containers! /usr/bin/env python3

import lxc
import sys
import os.path

temp = sys.argv
del temp[0:2]
for num in temp :
	lists = []
	if "-" in num :
		num = int(num.split("-"))
		num2 = 0
		for range(int(num[0]),int(num[1])+1) :
			lists.append(int(num[0])+num2)
			num2+=1
	else :
		lists.append(int(num))

con_name = lxc.list_containers()
con_obj = lxc.list_containers(as_object=True)
temp = sys.argv

if argvs[1] == "m" :
	num = 0
	while num < len(lists) :
		if con_obj[lists[num]-1] == "STOPPED" :
			print(con_name[lists[num]-1] + " | " + "Start "
								+str(con_obj[lists[num]-1].start()))
		else :
			stdn = con_obj[lists[num-1]].shutdown()
 			print(con_name[lists[num-1]] + " | " + "Shutdown "+str(stdn))
			if not stdn:
 				print(con_name[lists[num-1]] + " | " + "Stop "
								+str(con_obj[lists[num-1]].stop()))

		num += 1

if temp[1] == "g" :
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
			if con_obj[lists[num]-1] == "STOPPED" :
			print(con_name[lists[num]-1] + " | " + "Start "
								+str(con_obj[lists[num]-1].start()))
			else :
				stdn = con_obj[lists[num-1]].shutdown()
 				print(con_name[lists[num-1]] + " | " + "Shutdown "+str(stdn))
				if not stdn:
 					print(con_name[lists[num-1]] + " | " + "Stop "
								+str(con_obj[lists[num-1]].stop()))

if not temp[1] is None and not temp[1]=="g" and not temp[1]=="m":
		print("You must input the first argument as 'm' or 'g'.")
