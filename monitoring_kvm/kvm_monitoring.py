import sys,os,time
reload(sys)
sys.setdefaultencoding('utf8')

import monitoring_kvm_daemon
from tools import conf
from tools.check_client import *

cnf = conf.configure('/root/script/monitoring_kvm/tools/mointoring_kvm.conf')
retry = int(cnf.retry()) * int(cnf.response())

def write_file(content):
	with open('/root/script/monitoring_kvm/tools/check_client_conn','w') as f:
		f.writelines(content)
	

def start_server():
	start = monitoring_kvm_daemon.server_socket('/root/script/monitoring_kvm/tools/mointoring_kvm.conf')
	start.server_receive()

def local_do_work():
	start = monitoring_kvm_daemon.transnit_data('/root/script/monitoring_kvm/tools/mointoring_kvm.conf')
	data = start.data_collect()
	print "dddddddddddddd",data
	monitoring_kvm_daemon.local_do_working(data)
	el = 0
	write_file('0')
def start_client():
	while True:
		start  = monitoring_kvm_daemon.client_socket('/root/script/monitoring_kvm/tools/mointoring_kvm.conf')
		start.client_send()
		time.sleep(1)
		continue
		
def usage():
	usages='''
Usage:
	python kvm_monitoring.py [server role]
Example:
	python kvm_monitoring.py {server|work|client}
	'''
	print usages


if __name__ == '__main__':
	cnf = conf.configure('/root/script/monitoring_kvm/tools/mointoring_kvm.conf')
	flage = cnf.flage()
	#print "fff",flage
	if len(sys.argv) == 2:
		if (sys.argv[1] == 'server') and (flage == 'backup'):
			start_server()
		elif (sys.argv[1] == 'work') and (flage == 'backup'):
			local_do_work()
		elif (sys.argv[1] == 'client') and (flage == 'master'):
			start_client()
		else:
			print "You fill in the wrong state and wrong role"
	else:
		usage()
