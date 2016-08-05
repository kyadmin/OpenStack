import sys
reload(sys)
sys.setdefaultencoding('utf8')

from tools import log as logging
from tools import shell_cmd as shell

import os,time,libvirt
import socket,traceback
from tools import conf
from tools import action_kvm as action

filename='tools/monitoring_kvm.conf'
logfile = 'monitoring_kvm.log'
logdir = '/var/log/monitoring_kvm'

if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)

os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')

def exist_hostname():
	exist_host = []
	exist_cmd = "virsh list --all |grep -v -e Id -e '---' -e '^$'|awk '{print $2}'"
	result = shell.shell_cmd(exist_cmd)
	if not result:
		exist_host = ['NULL']
		return exist_host
	else:
		for i in xrange(len(result)):
			ap = result[i].split()[0]
			exist_host.append(ap)
		return exist_host



class server_socket:
	def __init__(self,filename=None):
		self.filename=filename
		cnf = conf.configure(self.filename)
		self.port = cnf.port()
		self.host = cnf.host()
		self.flage = cnf.flage()
		self.response = cnf.response()
		self.retry = int(cnf.retry()) * int(cnf.response())
	def server_receive(self):
		ip = self.host
		port = self.port
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		s.bind((ip,int(port)))
		s.listen(9)
		check_file = '/root/script/monitoring_kvm/tools/check_client_conn'
		try:
			while True:
				####################################
				# Process the connection
				try:
					clientconn,clientaddr=s.accept()
				except (KeyboardInterrupt, SystemExit):
					raise
					logging.error("you have CTRL+C,Now quit")
				except:
					traceback.print_exc()
					logging.error(traceback.print_exc())
				try:
					print "Got connection from %s",clientconn.getpeername() 
					logging.info("Got connection from %s", clientconn.getpeername())
					with open(check_file,'w') as f:
						f.writelines('1')
					while True:
						remote_data=clientconn.recv(8094)
						if not len(remote_data):
                            				clientconn.send('welcome',remote_data)
							logging.info(("The client data has been received and connection will be disconected!"))
                            				break
						clientconn.sendall(remote_data)
						recv_data = eval(remote_data)
						remote_data += remote_data
						print "Data is :",remote_data
						logging.debug(remote_data)#####
						self.do_working(recv_data)
				except (KeyboardInterrupt, SystemExit):
					raise
					logging.error("you have CTRL+C,Now quit")
				except:
					traceback.print_exc()
					logging.error(traceback.print_exc())
				# Close the connection
                		try:
					clientconn.close()
				except KeyboardInterrupt:
					raise
					logging.error("you have CTRL+C,Now quit")
                		except:
                    			traceback.print_exc()
					logging.error(traceback.print_exc())
		except (KeyboardInterrupt, SystemExit):
            		print "you have CTRL+C,Now quit"
			raise
			logging.error(traceback.print_exc())
        	except:
            		traceback.print_exc()
			logging.error(traceback.print_exc())
        	finally:
            		s.close()
	def  do_working(self,data):
		def list_all(data):
			conn = libvirt.open('qemu:///system')
			if isinstance(data,dict):
        			for x in range(len(data)):
            				temp_key = data.keys()[x]
            				a = data[temp_key]
            				#print  a.get('state')
            				if (a.get('state') == 'NULL') or (a.get('state') == 'fluent'):
                				b = a.get('id')
						name = a.get('hostname')
                				print "The virtual machine [%s] state for id [%s] do not need to do anying..." %(name,b)
						logging.info("The virtual machine [%s] state for id [%s] do not need to do anying..." %(name,b))
					elif (a.get('state') == 'active') or (a.get('state') == 'inactive'):
						c = a.get('id')
						name2 = a.get('hostname')
						start = action.startDomaction(conn,name2)
						if not start:
							print "The virtual machine [%s] state for id [%s] started successfully..." %(name2,c)
							logging.info("The virtual machine [%s] state for id [%s] stared successfully..." %(name2,c))
							cmd = 'sh /root/script/monitoring_kvm/tools/send_mail.sh  Successfully %s' % name2
							shell.shell_cmd(cmd)
						else:
							print "The virtual machine [%s] state for id [%s] started faild..." %(name2,c)
							logging.info("The virtual machine [%s] state for id [%s] stared faild..." %(name2,c))
							cmd = 'sh /root/script/monitoring_kvm/tools/send_mail.sh Faild %s' % name2
							shell.shell_cmd(cmd)
							
			conn.close()
		list_all(data)
		print "It is ok"
		
				
class client_socket:
        def __init__(self,filename):
		self.filename = filename
                cnf = conf.configure(self.filename)
                self.port = cnf.port()
                self.host = cnf.host()
                self.flage = cnf.flage()
                self.response = cnf.response()
		self.host_vm = cnf.hostname_vm()
		self.ip_vm = cnf.ip_vm()
		self.role_vm = cnf.role_vm()
	def client_send(self):
		#hello = 10
		hello = int(self.response)
		#print "respone.....",type(self.response)
		print "hello.....",type(hello)
		#print hello
		data = str(transnit_data(self.filename).data_collect())
		data_do = transnit_data(self.filename).data_collect()
		try:
			print data
			print "host is :",self.host
			print "port is :",self.port
			logging.info("Miontor agent started Successfully!")
			while True:
				self.do_working(data_do)
				try:
					host = self.host
					port = self.port
					s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
					s.connect((host,int(port)))
					logging.info(("Miontor agent has been successfully connected to the server!!"))
					s.sendall(data)
					logging.debug(data)
					buf = s.recv(8092)
					if not len(data): break
					s.close()
				except:
					logging.error('socket.error: [Errno 111] Connection refused')
					continue
				finally:
					time.sleep(hello)
		except:
			logging.error('The socket connect to the server failed!!!')
	
					
	def  do_working(self,data):
		#data = self.transnit_data()
		def list_all(data):
			conn = libvirt.open('qemu:///system')
			if isinstance(data,dict):
        			for x in range(len(data)):
            				temp_key = data.keys()[x]
            				a = data[temp_key]
            				#print  a.get('state')
            				if (a.get('state') == 'NULL') or (a.get('state') == 'fluent') or (a.get('state') == 'inactive'):
                				b = a.get('id')
						name = a.get('hostname')
                				print "The virtual machine [%s] state for id [%s] do not need to do anying..." %(name,b)
						logging.info("The virtual machine [%s] state for id [%s] do not need to do anying..." %(name,b))
					elif (a.get('state') == 'active'):
						c = a.get('id')
						name2 = a.get('hostname')
						stop = action.shutdownDomaction(conn,int(c))
						if not stop:
							print "The virtual machine [%s] state for id [%s] shutown successfully..." %(name2,c)
							logging.info("The virtual machine [%s] state for id [%s] shutdown successfully..." %(name2,c))
							cmd = 'sh /root/script/monitoring_kvm/tools/send_mail.sh  Successfully %s' % name2
							shell.shell_cmd(cmd)
						else:
							print "The virtual machine [%s] state for id [%s] shutown faild..." %(name2,c)
							logging.info("The virtual machine [%s] state for id [%s] shutdown faild..." %(name2,c))
							cmd = 'sh /root/script/monitoring_kvm/tools/send_mail.sh Faild %s' % name2
							shell.shell_cmd(cmd)
							
			conn.close()
		list_all(data)
		print "It is ok"

class transnit_data:
	def __init__(self,filename):
                self.filename = filename
                cnf = conf.configure(self.filename)
                self.port = cnf.port()
                self.host = cnf.host()
                self.flage = cnf.flage()
                self.response = cnf.response()
                self.host_vm = cnf.hostname_vm()
                self.ip_vm = cnf.ip_vm()
                self.role_vm = cnf.role_vm()

	def data_collect(self):
		data = {}
		list_title = []
		host = self.host_vm
		IP = self.ip_vm
		Role = self.role_vm
		#############################
		def host_id_associated():
			associated = []
			associated_cmd = "virsh list |grep -v -e Id -e  - -e  ^$|awk '{print $2,$1}'"
			result = shell.shell_cmd(associated_cmd)
			for i in xrange(len(result)):
				rs = result[i].split()
				associated.append(rs)
			return associated
		ID = host_id_associated()
		#print "host is :",host
		#print "IP IS :",IP
		#print "Role is :",Role
		#print "ID is :",ID
		#####################################
		def host_state_associated():
			conn = libvirt.open('qemu:///system')
			state_list = []
			for j in xrange(len(host.split(','))):
				if host.split(',')[j] in exist_hostname():
					aa = action.checkDom(conn,host.split(',')[j],IP.split(',')[j])
					state_list.append(aa)
				else:
					state_list.append('NULL')
			#print "It is ok."
			conn.close()
			return state_list
		State = host_state_associated()
		#list1 = ('openstack', '172.16.1.1', 55, 'Backup', 'active')
		#list2 =  ('openstack1', '172.16.1.2', 56, 'Backup', 'active')
		#list3 = ('openstack2', '172.16.1.3', 57, 'Backup', 'active')
		#list_title = [list1,list2,list3]
		#################################################
		# ID buqi
		host_num = len(host.split(','))
		ID_num = len(ID)
		if ID_num < host_num:
			chayi = host_num - ID_num
			count = 0
			while (count < chayi):
				ad = ['NULL','NULL']
				ID.append(ad)
				count = count + 1
		#################################################
                # IP buqi
                host_num = len(host.split(','))
                IP_num = len(IP.split(','))
                if IP_num < host_num:
                        chayi1 = host_num - IP_num
                        count1 = 0
                        while (count1 < chayi1):
                                ad = ['NULL','NULL']
                                ID.append(ad)
                                count1 = count1 + 1
		#################################################
                # State buqi
                host_num = len(host.split(','))
                State_num = len(State)
                if State_num < host_num:
                        chayi2 = host_num - State_num
                        count2 = 0
                        while (count2 < chayi2):
                                ad = ['NULL','NULL']
                                ID.append(ad)
                                count2 = count2 + 1
		#print "host1 is :",host
		#print "IP1 IS :",IP
		#print "Role1 is :",Role
		#print "ID1 is :",ID

		for i in xrange(host_num):
			#if (host.split(',')[i] == ID[i][0]) and (host.split(',')[i] == State[i][0]):
			#if (host.split(',')[i] == ID[i][0]) :
			list_a = (host.split(',')[i],IP.split(',')[i],ID[i][1],Role,State[i])
        		list_title.append(list_a)
					
		#print "list_titel is:",list_title

		for host,IP,ID,Role,State in list_title:
			data.setdefault(host,{})['ip'] = IP
			data.setdefault(host,{})['id'] = ID
			data.setdefault(host,{})['role'] = Role
			data.setdefault(host,{})['state'] = State
			data.setdefault(host,{})['hostname'] = host
		return data

def  local_do_working(data):
	def list_all(data):
		conn = libvirt.open('qemu:///system')
		if isinstance(data,dict):
        		for x in range(len(data)):
            			temp_key = data.keys()[x]
            			a = data[temp_key]
            			#print  a.get('state')
            			if (a.get('state') == 'NULL') or (a.get('state') == 'fluent'):
                			b = a.get('id')
					name = a.get('hostname')
                			print "The virtual machine [%s] state for id [%s] do not need to do anying..." %(name,b)
					logging.info("The virtual machine [%s] state for id [%s] do not need to do anying..." %(name,b))
				elif (a.get('state') == 'inactive'):
					c = a.get('id')
					name2 = a.get('hostname')
					start = action.startDomaction(conn,name2)
					if not start:
						print "The virtual machine [%s] state for id [%s] started successfully..." %(name2,c)
						logging.info("The virtual machine [%s] state for id [%s] stared successfully..." %(name2,c))
						cmd = 'sh /root/script/monitoring_kvm/tools/send_mail.sh  Successfully %s' % name2
						shell.shell_cmd(cmd)
					else:
						print "The virtual machine [%s] state for id [%s] started faild..." %(name2,c)
						logging.info("The virtual machine [%s] state for id [%s] stared faild..." %(name2,c))
						cmd = 'sh /root/script/monitoring_kvm/tools/send_mail.sh Faild %s' % name2
						shell.shell_cmd(cmd)
				elif (a.get('state') == 'active'):
					d = a.get('id')
					name3 = a.get('hostname')
					reset = action.resetDom(conn,int(d))
					if not reset:
						print "The virtual machine [%s] state for id [%s] reset successfully..." %(name3,d)
						logging.info("The virtual machine [%s] state for id [%s] reset successfully..." %(name3,d))
						cmd = 'sh /root/script/monitoring_kvm/tools/send_mail.sh  Successfully %s' % name3
						shell.shell_cmd(cmd)
					else:
						print "The virtual machine [%s] state for id [%s] reset faild..." %(name3,d)
						logging.info("The virtual machine [%s] state for id [%s] reset faild..." %(name3,d))
						cmd = 'sh /root/script/monitoring_kvm/tools/send_mail.sh Faild %s' % name3
						shell.shell_cmd(cmd)
							
		conn.close()
	list_all(data)
	print "It is ok"
