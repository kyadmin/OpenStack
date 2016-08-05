#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import time
import sys
import traceback
import os
import socket
from otomat.conf import conf
from threading import *
from Queue import Queue
from otomat.sql import otomat_sql
from  otomat.logs  import log as logging
queue=Queue() #create queue
#
cnf =conf.files_conf_check('/etc/otomat/otomat.cnf')
logfile = cnf.server_log()
logdir = cnf.server_logdir()

if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)

os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')


'''
class recive_report:
	def __init__(self,report_file = "/tmp/report",filename = None,data= None):
		#self.filename = filename
		#cnf = conf.files_conf_check(self.filename)
		#self.path = cnf.server_report_path()
		self.report = report_file
		self.data = data
	def  report(self):
		print self.report
		print self.data
		#os.chdir(self.path)
		f = open(self.report,'w+')
		f.writelines(self.data)
		traceback.print_exc()
		f.close()
'''


#

class active_server:
	def __init__(self, filename="otomat.cnf"):
		#recive_report.__init__(self)
		self.filename = filename
		cnf = conf.files_conf_check(self.filename)
		self.port = cnf.server_port()
		self.host = cnf.server_ip()
		self.sql_host = cnf.sql_host()
		self.sql_user = cnf.sql_user()
		self.sql_password = cnf.sql_password()
		self.sql_defdb = cnf.sql_defaultdb()
		#ThreadPool
		self.MaxThreads = cnf.server_worker()
		#self.lockpool = Lock()
		#self.queue = []
		#self.sem = Semaphore(0)
	def  handleconnection(self,clientconn):
		"""handle an incoming connection."""
		logging.info("Received new Client %s connection.",  clientconn.getpeername())
		try:
			logging.debug("Got connection from %s",  clientconn.getpeername())
			if (active_count()-1) >= self.MaxThreads:
				clientconn.close()
				return
			"""Main loop of client-process threads."""
			name = current_thread().getName()
			clientconn.sendall('Greetings. You are being serviced by recviled' )
			while True:
				data = clientconn.recv(4096)
				if  not len(data):
					logging.warning(("Did not receive the client data!"))
					break

				clientconn.sendall(data)
				recv_data = eval(data)
				#print   data
				print recv_data
				logging.debug(data)
				self.pysql(recv_data)
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			traceback.print_exc()
		#close the connection
		try:
			clientconn.close()
		except KeyboardInterrupt:
			raise
		except:
			traceback.print_exc()

	def  startthread(self):
		# Called by handleconnection when a new thread is need.
		# Note:lockpool is already acquired when this fuction is called.
		logging.info(("Starting netw Client processor thread."))
		global queue
		threads = []
		pool = self.MaxThreads
		t = Thread(target = self.handleconnection(),args = (clientconn,queue))
		for x in xrange(1, pool+1):
			threads.append(t)
		for i in threads:
			t.setDaemon(1)
			t.start()
			#time.sleep(0.1)
		#queue.join()
       	# write data for file
	"""
	def  report(self,data):

	        f = open('/tmp/report',"ab")
	        try:
		    f.writelines(data)
	        except IOError:
		    traceback.print_exc()
	        finally:
		    f.close()
	"""
	def  pysql(self,recv_data):
		data = recv_data
		hostname = self.sql_host
		username = self.sql_user
		password = self.sql_password
		defdata = self.sql_defdb
		mysql = otomat_sql.PyMysql()
		mysql.newConnection(
			host=hostname,user=username,
			passwd=password,defaultdb=defdata)
		sqltext = "insert into `report_list` (HostName,Host_ip,Time,Cpu_Utilization,Mem_total,Mem_free,\
			Mem_used,Mem_percent,Swap_total,Swap_free,Swap_used,\
			Swap_percent,Disk_total,Disk_used,Disk_free,Disk_percent,\
			Network_traffic_recv,Network_traffic_sent) value (\
			%s,%s,(NOW()),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

		#args = [('client','172.16.209.219','0.0','1036570','389505024L',
		#	'647065600L','15.300000000000001','2080370688L','2080370688L',
		#	'0L','0.0','30414569','2494730240','47665602560',
		#	'4.7000000000000002','30414569','81069')]
		hostname = data['hostname']
		hostip = data['host_ip']
		cpu_utilization = str(data['cpu_percent'])
		mem_total = str(data['mem_total'])
		mem_free = str(data['mem_free'])
		mem_used = str(data['mem_used'])
		mem_percent = str(data['mem_percent'])
		swap_total = str(data['swap_total'])
		swap_free = str(data['swap_free'])
		swap_used = str(data['swap_used'])
		swap_percent = str(data['swap_percent'])
		disk_total = str(data['disk_total'])
		disk_used = str(data['disk_used'])
		disk_free = str(data['disk_free'])
		disk_percent = str(data['disk_percent'])
		nic_recv = str(data['network_recv'])
		nic_sent = str(data['network_sent'])
		args = [(hostname,hostip,cpu_utilization,mem_total,mem_free,
			mem_used,mem_percent,swap_total,swap_free,swap_used,
			swap_percent,disk_total,disk_used,disk_free,disk_percent,
			nic_recv,nic_sent)]
		mysql.execute(sqltext,args,mode=otomat_sql.DICTCURSOR_MODE)
	def listener(self):
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		s.bind((self.host,int(self.port)))
		s.listen(5)
		logging.info(("The otomat-server has been launched successfully "))
		while True:
			try:
				clientconn, clientaddr = s.accept()
			except (KeyboardInterrupt,SystemError):
				raise
				logging.error(("The otomat-server start  failure"))
			except:
				traceback.print_exc()
				logging.error(trackback.print_exc())
				logging.error(("The otomat-server start  failure"))
				continue
			self.handleconnection(clientconn)




#if __name__=="__main__":
#	data = '''
#	Welcome to china  lllllllllllllllllllllllllllll
#	'''
#	report(data)
#	#t = recive_report(data)
#	#t.report()

def main(argv=sys.argv[1:]):
	t1 = active_server(argv)
	t1.listener()
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

