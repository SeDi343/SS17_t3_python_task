#!/usr/bin/env python3

# ! Python Status Monitor Task
#
# \description A Python Status Monitor
#
# \author Sebastian Dichler <el16b032@technikum-wien.at> <sedi343@gmail.com>
#
# \version Rev.: 01, 09.06.2017 - Created the py file
#          Rev.: 02, 09.06.2017 - Formated User output
#

import sys
import psutil
import os
import time
import datetime

# \033[1m

debug = 0

def clear():
	os.system("cls" if os.name == "nt" else "clear")

def secs2hours(secs):
	mm, ss = divmod(secs, 60)
	hh, mm = divmod(mm, 60)
	return "%d:%02d:%02d" % (hh, mm, ss)

core_logic = psutil.cpu_count()
core_nologic = psutil.cpu_count(logical=False)

while True:
	
# COLLECT SYSTEM INFORMATION
	
	cpu_percent_full = psutil.cpu_percent()
	cpu_percent = psutil.cpu_percent(percpu=True)
	cpu_frequency = psutil.cpu_freq()
	cpu_temp = psutil.sensors_temperatures()
	cpu_fan = psutil.sensors_fans()
	disk = psutil.disk_usage('/')
	battery = psutil.sensors_battery()
	users = psutil.users()
	
# CLEAR SCREEN
	
	clear()
	
# TERMINAL OUTPUT
	
	print("System Status Monitor el16b032 BEL2 2017\n")
	
	print(core_logic, "logical cores", core_nologic, "physical cores")
	print("")
	
# PRINT SYSTEM INFORMATION
	
	print("CPU Percentage\t\t", cpu_percent_full,"%", cpu_percent)
	print("CPU Frequency\t\t",
			"current:", cpu_frequency[0], "\n\t\t\t",
			"min:", cpu_frequency[1], "\n\t\t\t",
			"max:", cpu_frequency[2])
	print("")
	
	print("Disk usage\t\t", disk[3])
	print("")
	
	print("CPU Temperature\t\t")
	names = set(list(cpu_temp.keys()))
	for name in names:
		if name == "coretemp":
			for entry in cpu_temp[name]:
				print("\t\t\t", entry.label or name,
						entry.current,
						entry.high,
						entry.critical)
	print("")
	
	for key in cpu_fan:
		print("CPU Fanspeed Right\t", cpu_fan[key][0][1], "rpm")
		print("CPU Fanspeed Left\t", cpu_fan[key][1][1], "rpm")
	print("")
	
	print("Battery\t",
		"capacity\t", battery[0], "\n\t",
		"time left\t", secs2hours(battery[1]))
	print("")
	
	print("Username\t\t", users[0][0])
	print("Host\t\t\t", users[0][2])

	
	time.sleep(1)
