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
#          Rev.: 04, 09.06.2017 - Added online user ammount
#          Rev.: 05, 09.06.2017 - Added singal handler for ctrl-c
#          Rev.: 06, 27.06.2017 - Adding try/exceptions
#
# \information Information from
#              https://pythonhosted.org/psutil/
#              https://stackoverflow.com/questions/14319023/find-out-who-is-logged-in-on-linux-using-python
#              https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python
#


################################################################################
# I M P O R T   L I B R A R Y S                                                #
################################################################################

import sys
import psutil
import os
import time
import datetime
import signal

################################################################################
# F U N C T I O N S                                                            #
################################################################################

def clear():
	os.system("cls" if os.name == "nt" else "clear")

def secs2hours(secs):
	mm, ss = divmod(secs, 60)
	hh, mm = divmod(mm, 60)
	return "%d:%02d:%02d" % (hh, mm, ss)

def signal_handler(signal, frame):
	print("You pressed Ctrl+C!")
	sys.exit(0)

################################################################################
# R E C E I V E   O N E   T I M E   N E E D E D   V A L U E S                  #
################################################################################
# CPU ammount logical
try:
	core_logic = psutil.cpu_count()
except:
	core_logic = "\033[1mNO DATA RECEIVED\033[0m"

# CPU ammount physical
try:
	core_nologic = psutil.cpu_count(logical=False)
except:
	core_nologic = "\033[1mNO DATA RECEIVED\033[0m"

################################################################################
# R E C E I V E   V A L U E S                                                  #
################################################################################

signal.signal(signal.SIGINT, signal_handler)
while True:
# CPU overall percentage
	try:
		cpu_percent_full = psutil.cpu_percent(interval=None)
	except:
		cpu_percent_full = "\033[1mNO DATA RECEIVED\033[0m"
	
# CPU percentage per cpu
	try:
		cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
	except:
		cpu_percent = "\033[1mNO DATA RECEIVED\033[0m"
	
# CPU frequency
	try:
		cpu_frequency = psutil.cpu_freq()
	except:
		cpu_frequency = "\033[1mNO DATA RECEIVED\033[0m"
	
# CPU temperarature
	try:
		cpu_temp = psutil.sensors_temperatures()
	except:
		cpu_temp = "\033[1mNO DATA RECEIVED\033[0m"
	
# MEMORY information
	try:
		memory = psutil.virtual_memory()
	except:
		memory = "\033[1mNO DATA RECEIVED\033[0m"
	
# CPU fan
	try:
		cpu_fan = psutil.sensors_fans()
	except:
		cpu_fan = "\033[1mNO DATA RECEIVED\033[0m"
	
# DISK information
	try:
		disk = psutil.disk_usage('/')
	except:
		disk = "\033[1mNO DATA RECEIVED\033[0m"
	
# BATTERY information
	try:
		battery = psutil.sensors_battery()
	except:
		battery = "\033[1mNO DATA RECEIVED\033[0m"
	
# USERS logged in user
	try:
		users = psutil.users()
	except:
		users = "\033[1mNO DATA RECEIVED\033[0m"
	
# USERS ammount of logged in users
	try:
		userammount = os.popen('who | wc -l').read()
		userammount = userammount.rstrip()
	except:
		userammount = "\033[1mNO DATA RECEIVED\033[0m"
	
################################################################################
# C L E A R   S C R E E N                                                      #
################################################################################
	
	clear()
	
################################################################################
# T E R M I N A L   O U T P U T                                                #
################################################################################
	
# HEADERBAR
	print("\033[1mSystem Status Monitor / el16b032 / BEL2 2017\033[0m\n")
	print("Hello\033[1m", users[0][0], "\033[0mThere", userammount, "users online")
	
	print("You have\033[1m", core_logic, "\033[0mlogical cores and\033[1m", core_nologic, "\033[0mphysical cores")
	if memory.available <= 100 * 1024 * 1024:
		print("\033[1mWarning: Less Memory available:", memory.available, "\033[0m")
	
	print("")
	
# PRINT CPU INFORMATION
	
	print("CPU Percentage\t\t\033[1m", cpu_percent_full,"%\033[0m", cpu_percent)
	print("CPU Frequency\t\t",
			"current:\033[1m", cpu_frequency.current, "\033[0m\n\t\t\t",
			"min:", cpu_frequency.min, "\n\t\t\t",
			"max:", cpu_frequency.max)
	print("")
	
# PRINT CPU TEMPERATURE INFORMATION
	
	names = set(list(cpu_temp.keys()))
	for name in names:
		if name == "coretemp":
			for entry in cpu_temp[name]:
				print("CPU Temperature\t\t", entry.label or name,
						"\033[1m", entry.current, "\033[0m",
						entry.high,
						entry.critical)
	print("")
	
# PRINT DISK INFORMATION
	
	print("Disk usage\t\t\033[1m", disk.percent, "\033[0m")
	print("")
	
# PRINT FAN SPEED INFORMATION
	
	for name, entries in cpu_fan.items():
		for entry in entries:
			print("Fanspeed", entry.label or name, "\t\033[1m", entry.current, "rpm\t\033[0m")
	print("")
	
# PRINT BATTERY INFORMATION
	
	print("Battery\t",
		"capacity\t\033[1m", battery.percent, "\033[0m\n\t",
		"time left\t", secs2hours(battery.secsleft))
	print("")
	
# PRINT USER AND HOSTNAME
	
	for i in range(0, len(users)):
		print("Username\t\t\033[1m", users[i].name, "\033[0m@", users[i].host)
	
	time.sleep(1)
signal.pause()
