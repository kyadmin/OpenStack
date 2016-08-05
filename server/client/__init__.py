#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os,re
import time
import sys
import StringIO
import socket
import pickle
from otomat.conf import conf
from otomat.collection import systemmonitor

#
def os_release_ubuntu():
        s = os.uname()[3]
        a = re.search("Ubuntu",s)
        return a.group()
def os_release_centos():
        s = []
        f = open('/etc/redhat-release')
        s = f.read()
        return s.split()[0]

class active_agent:
	def __init__(self, filename = '/etc/otomat/otomat.cnf'):
		self.filename = filename
		cnf = conf.files_conf_check(self.filename)
		self.port = cnf.server_port()
		self.host = cnf.server_ip()
		self.client_nic = cnf.nic_port()

	def  handleconnection(self):
		data = str(self.transnit_data())
		while True:
               		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.connect((self.host,int(self.port)))
    			s.sendall(data)
			#print data
			#data = "#" * 1024
			buf = s.recv(8092)
			if not len(buf):
				break
			s.close()
			time.sleep(10)
			continue

	def transnit_data(self):
		data = {}
		collect = systemmonitor.Monitor_systeminfo()
		# cpu
		cpu_percent = collect.Cpu_Percent()
		# mem
		mem_total = collect.Mem_info().total
		mem_free = collect.Mem_info().free
		mem_used = collect.Mem_info().used
		mem_percent = collect.Mem_info().percent
		swap_total = collect.Swap_info().total
		swap_free = collect.Swap_info().free
		swap_used = collect.Swap_info().used
		swap_percent = collect.Swap_info().percent
		# disk
		disk_total = collect.disk_usage().total
		disk_free = collect.disk_usage().free
		disk_used = collect.disk_usage().used
		disk_percent = collect.disk_usage().percent
		# network nic I/O
                if os_release_ubuntu() == "Ubuntu" :
		        network_recv = collect.nic_io_ubuntu().bytes_recv
		        network_sent = collect.nic_io_ubuntu().bytes_sent
                elif os_release_centos() == "Centos":
		        network_recv = collect.nic_io_centos().bytes_recv
		        network_sent = collect.nic_io_centos().bytes_sent
                else:
                        pass
		# hostname and ipaddress
		host = collect.hostname()
		ifname = self.client_nic
		#ip_address = collect.get_ip_address(ifname)
		ip_address = '172.16.209.243'
		#
		L1 = ['cpu_percent','mem_total','mem_free','mem_used',
			'mem_percent','swap_total','swap_free','swap_used',
			'swap_percent','disk_total','disk_free','disk_used',
			'disk_percent','network_recv','network_sent','hostname',
			'host_ip']
		L2 = [cpu_percent,mem_total,mem_free,mem_used,mem_percent,
			swap_total,swap_free,swap_used,swap_percent,disk_total,
			disk_free,disk_used,disk_percent,network_recv,network_sent,
			host,ip_address]


		data = dict(zip(L1[::],L2))
		#print data
		#data = 'hello,word'
		return data







#if __name__=="__main__":

#	t = active_agent()
#	t.transnit_data()


def main(argv=sys.argv[1:]):
	t = active_agent(argv)
	t.handleconnection()
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
