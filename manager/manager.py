#st_containers! /usr/bin/evv python3

import lxc
import sys

machine_name = lxc.list_containers()
print ('\nMachine list')
con_obj = lxc.list_containers(as_object=True)

num = 0
while num < len(machine_name):
	args ="  " + str(num+1) + ": " +  machine_name[num] + " " + con_obj[num].state
	print(args)
	num += 1

print('\n1.Start : 2.Stop : 0.Exit')

menu = int(input('Please select menu ->'))

if menu == 1:
	select = (input('\nWhich machine do you want to start? ->')).split()
	num = 0
	while num < len(select):
		select[num] = int(select[num])
		if select[num] == 0:
			num2 = 0
			while num2 < len(machine_name):
				print(machine_name[num2] + ":" + str(con_obj[num2].start()))
				num2 += 1
		else:					
			print(machine_name[select[num]-1] + ":" + str(con_obj[select[num]-1].start()))
		num+=1

if menu == 2:
	select = (input('\nWhich machine do you want to shutdown? ->')).split()
	num = 0
	while num < len(select):
		select[num] = int(select[num])
		if select[num] == 0:
			num2 = 0
			while num2 < len(machine_name):
				stdn = con_obj[num2].shutdown()
				print (machine_name[num2] + ":" + str(stdn))
				if not stdn :
					print(machine_name[num2] + ":" + str(con_obj[num2].stop()))
				num2 += 1
		else:
			stdn = con_obj[select[num]-1].shutdown()
			print(machine_name[select[num]-1] + ":" + str(stdn))
			if not stdn :
				print(machine_name[select[num]-1] + ":" + str(con_obj[select[num]-1].stop()))
		num += 1

