#!/usr/bin/python
#
#========================================================================
# Author:Andre
# Email:wangyouyan2146@gmail.com
# File Name: 
# Description:
# Edit History:
# 2015-03-18 File created.
#========================================================================
import sys
import time
import os

logfile_local = "login.log"
logfile_remote = "remote_log.log"
logdir = "/tmp/pyexpect_log"

if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)


import pxssh
import getpass
def print_clour():
	print '\033[1;31;40m'
	print '*' * 100
	print '* Welcome Use Test TO Login '
	print ''
	print '*' * 100
	print '\033[0m'

def ssh_login():
	try:
		while True:
			s = pxssh.pxssh()
			print_clour()
			hostname = raw_input('hostname: ')
			username = raw_input('username: ')
			password = getpass.getpass('password: ')
			s.login(hostname, username, password)
			cmd = raw_input('commnd[exit:EOF]:')
			if  (cmd == "EOF") and  (cmd == "eof"):
					break
			else :
				s.sendline(cmd)   # run a command
				s.prompt()        # match the prompt
				print(s.before)        # print everything before the prompt.
			s.logout()
	except pxssh.ExceptionPxssh as e:
		print("pxssh failed on login.")
		print(e)
if __name__ == "__main__":
	ssh_login()

