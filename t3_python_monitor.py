#!/usr/bin/env python3

# ! Python Status Monitor Task
#
# \description A Python Status Monitor
#
# \author Sebastian Dichler <el16b032@technikum-wien.at> <sedi343@gmail.com>
#
# \version Rev.: 01, 09.06.2017 - Created the py file
#          Rev.: 02, 09.06.2017 - Formated User output
#          Rev.: 03, 09.06.2017 - Better formating and better use of values like
#                                 cpu_frequency.current instead of
#                                 cpu_frequency[3]
#
# \information Information from
#              https://pythonhosted.org/psutil/
#              https://stackoverflow.com/questions/14319023/find-out-who-is-logged-in-on-linux-using-python
#

import sys
import psutil
import os
import time
import datetime
from subprocess import Popen, PIPE, STDOUT

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
	
	cpu_percent_full = psutil.cpu_percent(interval=None)
	cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
	cpu_frequency = psutil.cpu_freq()
	cpu_temp = psutil.sensors_temperatures()
	memory = psutil.virtual_memory()
	cpu_fan = psutil.sensors_fans()
	disk = psutil.disk_usage('/')
	battery = psutil.sensors_battery()
	users = psutil.users()
	userammount = os.popen('who | wc -l').read()
	userammount = userammount.rstrip()
	
# CLEAR SCREEN
	
	clear()
	
# TERMINAL OUTPUT
	
	print("\033[1mSystem Status Monitor / el16b032 / BEL2 2017\033[0m\n")
	print("Hello\033[1m", users[0][0], "\033[0mThere", userammount, "users online")
	
	print("\033[1m", core_logic, "\033[0mlogical cores and\033[1m", core_nologic, "\033[0mphysical cores")
	if memory.available <= 100 * 1024 * 1024:
		print("Warning: Less Memory available:", memory.available)
	
	print("")
	
# PRINT SYSTEM INFORMATION
	
	print("CPU Percentage\t\t\033[1m", cpu_percent_full,"%\033[0m", cpu_percent)
	print("CPU Frequency\t\t",
			"current:\033[1m", cpu_frequency.current, "\033[0m\n\t\t\t",
			"min:", cpu_frequency.min, "\n\t\t\t",
			"max:", cpu_frequency.max)
	print("")
	
	
	print("Disk usage\t\t\033[1m", disk.percent, "\033[0m")
	print("")
	
	
	
	names = set(list(cpu_temp.keys()))
	for name in names:
		if name == "coretemp":
			for entry in cpu_temp[name]:
				print("CPU Temperature\t\t", entry.label or name,
						"\033[1m", entry.current, "\033[0m",
						entry.high,
						entry.critical)
	print("")
	
	
	for name, entries in cpu_fan.items():
		for entry in entries:
			print("Fanspeed", entry.label or name, "\t\033[1m", entry.current, "\t\033[0m")
	print("")
	
	
	print("Battery\t",
		"capacity\t\033[1m", battery.percent, "\033[0m\n\t",
		"time left\t", secs2hours(battery.secsleft))
	print("")
	
	
	print("Username\t\t\033[1m", users[0][0], "\033[0m@", users[0][2])
	
	
	
	time.sleep(1)
