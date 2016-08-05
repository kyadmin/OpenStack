#_*_ coding: UTF-8 _*_
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import  ConfigParser

class configure:
	'''
	这是一个配置文件的模块,它可以提供mointoring_kvm.conf配置文件
     需要提供给程序所需的参数,示例如下:
	from tools import conf
	cfg = conf.configure('mointoring_kvm.conf')
	cfg.host()
	172.16.13.253
	'''
	def __init__(self,filename):
		self.filename = filename
		self.conf = ConfigParser.ConfigParser()
		self.conf.read(self.filename)
		s = self.conf.sections()
	# server 
	def host(self):
		s_host = self.conf.get("server","host")
		return s_host
	def port(self):
		s_port = self.conf.get("server","port")
		return s_port
	def flage(self):
		s_f = self.conf.get("server","flage")
		return s_f
	def response(self):
		s_response = self.conf.get("server","hello")
		return s_response
	def retry(self):
		s_retry = self.conf.get("server","retry")
		return s_retry
	# vm
	def hostname_vm(self):
		s_hostname = self.conf.get("vm","hostname")
		return s_hostname
	def ip_vm(self):
		s_ip = self.conf.get("vm","ip")
		return s_ip
	def role_vm(self):
		s_back = self.conf.get("vm","role")
		return s_back
