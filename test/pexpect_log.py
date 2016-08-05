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
import pexpect
import logging
import sys
import time
import os

logfile_local = "login.log"
logfile_remote = "remote_log.log"
logdir = "/tmp/pyexpect_log"

if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)



class running:
	def __init__(self,cmd=None,logfile=logfile_local):
		self.cmd = cmd
		self.logfile = logfile
	def run(self):
		run = pexpect.run(self.cmd)
		return run
	def log_record(self):
		f = file(self.logfile,'a')
		f.writelines(self.run())
		f.close()
		r = open(self.logfile)
		return r.readlines()		
class expect:
	def ssh_login(self,user='root',server='172.16.209.134',passwd='che001',cmd='date'):
		ret = -1
		child = pexpect.spawn('ssh %s@%s "%s"' % (user,server,cmd) )
		try:
			i = child.expect(['password:','continue connecting (yes/no)?'],timeout=5)
			if i == 0:
				child.sendline(passwd)
			elif i == 1:
				child.sendline('yes\n')
				child.expect('password:')
				child.sendline(passwd)
			child.sendline(cmd)
			r = child.read()
			print r
			ret = 0
		except pexpect.EOF:
			print "EOF"
			child.close()
			ret = -1
		except pexpect.TIMEOUT:
			print "TIMEOUT"
			child.close()
			ret = -2
		return ret


		

if __name__ == "__main__":
	cmd = sys.argv[1]
	p = expect()
	p.ssh_login(cmd)
	'''
	p = running(cmd)
	p.log_record()
	'''
