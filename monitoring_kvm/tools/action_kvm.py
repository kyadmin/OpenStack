#!/usr/bin/python
from __future__ import print_function
#
#========================================================================
# Author:Andre
# Email:wangyouyan2146@gmail.com
# File Name: 
# Description:
# Edit History:
# 2015-09-22 File created.
#========================================================================


import sys,os
reload(sys)
sys.setdefaultencoding('utf8')

from tools import log as logging
from tools import shell_cmd as shell
import libvirt

logfile = 'monitoring_kvm.log'
logdir = '/var/log/monitoring_kvm'

if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)

os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')


def createConnection():
	conn = libvirt.open('qemu:///system')
	if conn == None:
		print('Failed to open connection to qemu:///system',file=sys.stderr)
		logging.error('Failed to open connection to qemu:///system',file=sys.stderr)
		exit(1)

	else:
		print('--Connection is created successfully--')
		logging.info('--Connection is created successfully--')
	return conn

def closeConnection(conn):
	try:
		conn.close()
	except:
		print('Failed to close the connection.')
		logging.error('Failed to close the connection.')
		return 1
	
	print('Connection is closed...')
	logging.info('Connection is closed...')
def getDomInfoByName(conn):
	print('----get domain info by name -----')
	logging.debug('----get domain info by name -----')
	try:
		#myDom = conn.lookupByName(name)
		myDom = conn.listDefinedDomains()
		return myDom
	except:
		print('Failed to find the domain with name %s' % name)
		logging.error('Failed to find the domain with name %s' % name)
		return 1

def getDomInfoByID(conn):
	print('----get domain info by ID -----')
        logging.debug('----get domain info by ID -----')
        try:
		#myDom = conn.lookupByID(id)
		myDom = conn.listDomainsID()
		return myDom
	except:
                print('Failed to find the domain with ID %s' % id)
                logging.error('Failed to find the domain with ID %s' % id)
                return 1
def shutdownDomaction(conn,ID):
	print('----Shutdown domain info by ID -----')
	logging.debug('----Shutdown domain info by ID -----')
	dom = conn.lookupByID(ID)
	try:
		dom.destroy()
		print('Dom %s State %s' %(dom.name(),dom.info()[0]))
		logging.info('Dom %s State %s' %(dom.name(),dom.info()[0]))
		return 0
	except:
		print('Dom %s shutdown failed...' % dom.name())
		logging.error('Dom %s shutdown failed...' % dom.name())
		return 1	
		
		
def startDomaction(conn,name):
        print('----Start domain info by Name -----')
        logging.debug('----Start domain info by Name -----')
        dom = conn.lookupByName(name)
        try:
		dom.create()
		print('Dome %s boot sucessfully' %dom.name())
		logging.info('Dome %s boot sucessfully'%dom.name())
		return 0
	except:
		print('Dome %s boot failed' %dom.name())
		logging.error('Dome %s boot failed' %dom.name())
		return 1

def checkDom(conn,name,ip):
	print('---check Domin status-----')
	logging.info('---check Domin status-----')
	def check_ip(ip):
		cmd = 'fping %s' %ip
		ping_result = shell.shell_cmd(cmd)[0]
		if 'alive' in ping_result:
			return 'active'
		else:
			return 'inactive'
	dom = conn.lookupByName(name)
	try:
		if (dom.state() == [1,1]) and (check_ip(ip) == 'active'):
			return 'fluent'
		elif (dom.state() == [1,1]) or (check_ip(ip) == 'inactive'):
			return 'active'
		else:
			return 'inactive'
			
	except:
		print('Dom %s check failed...' %dom.name())
		logging.error('Dom %s check failed...' %dom.name())

def resetDom(conn,ID):
	print('---Reset Domin status-----')
	logging.info('---Reset Domin status-----')
        dom = conn.lookupByID(ID)
        try:
                dom.reset()
                print('Dom %s State %s' %(dom.name(),dom.info()[0]))
                logging.info('Dom %s State %s' %(dom.name(),dom.info()[0]))
                return 0
        except:
                print('Dom %s reset failed...' % dom.name())
                logging.error('Dom %s reset failed...' % dom.name())
                return 1

