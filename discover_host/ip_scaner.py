#!/usr/bin/python
import nmap
import sys
import time
import threading

class nmap_scan:
	def __init__(self,msg='172.16.209.1,172.16.209.254',port=22,arg='-sT'):
		#msg='172.25.0.1,172.25.0.254'
		num_msg = msg.split(',')
		self.ip_msg_small= num_msg[0].split('.')
		self.ip_msg_big = num_msg[1].split('.')
		self.big_msg=int(self.ip_msg_big[3])
		self.small_msg=int(self.ip_msg_small[3])
		self.result = self.big_msg - self.small_msg
		self.port = port
		self.arg = arg
		#print self.rseult

	def nmap_scan(self,ip,port,arg):
		np =  nmap.PortScanner()
		np.scan(ip,arguments='-p %s %s' %(port,arg))
		hosts_list = [(x, np[x][u'tcp'][port]['state']) for x in np.all_hosts()]
		for host, status in hosts_list:
			n = ('{0}:{1}'.format(host, status))
			print n



	def thread_nmap(self,n):
		arg = self.arg
		port = self.port
		ip_a = self.ip_msg_small[0] 
		ip_b = self.ip_msg_small[1] 
		ip_c = self.ip_msg_small[2]
		ip_d = '.'
		ip = ip_a + ip_d + ip_b + ip_d + ip_c + ip_d + str(n)
		#print "ip is %s; port is %s; arg is %s" % (ip,port,arg)
		threadname = threading.currentThread().getName()
		self.nmap_scan(ip,port,arg)


	def batch_nmap_scan(self):
		num = self.result
		#print num
		threads = []
	
		for x in xrange(1,num+1):
			threads.append(threading.Thread(target=self.thread_nmap ,args=(x,)))
		for t in threads:
			t.start()
			time.sleep(0.1)
		for t in threads:
			t.join()

	
if __name__ == '__main__':
	#msg = sys.argv[1]
	p = nmap_scan()
	p.batch_nmap_scan()



