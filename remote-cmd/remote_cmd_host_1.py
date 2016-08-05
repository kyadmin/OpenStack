#_*_ coding: UTF-8 _*_
import paramiko
import sys,os,time
import  ConfigParser

reload(sys)
sys.setdefaultencoding('utf8')

class files_conf:
 	def __init__(self,filename):
                self.filename = filename
                # 生产config 对象
                self.conf = ConfigParser.ConfigParser()
                # 用config对象读取配置文件
                self.conf.read(self.filename)
                # 以列表的形式返回section
                s = self.conf.sections()


        def username(self):
		o_user = self.conf.get("host_user","user_root")
		return o_user
	def address(self):
		o_address = self.conf.get("host_address","host")
		return o_address
	def password(self):
                # 得到指定的sections, options
                o_password = self.conf.get("host_password","password")
		return  o_password

class ssh_cmd(files_conf):
	def __init__(self,filename,command):
		files_conf.__init__(self,filename)
		inherit = files_conf(filename)
		self.hostname = inherit.address()
		self.username = inherit.username()
		self.password = inherit.password()
		self.command = command
		#self.cmd = 'ifconfig'
	def ssh_login_do(self):
		paramiko.util.log_to_file('paramiko.log')
		s = paramiko.SSHClient()
		s.load_system_host_keys()
		s.connect(username=self.username,password=self.password,hostname=self.hostname)
		stdin, stdout, stderr = s.exec_command(self.command)
		print stdout.read()
		s.close()
if __name__ == '__main__':
#        t=ssh_cmd('test.list','df')
#	t.ssh_login_do()
	from optparse import OptionParser
	parser = OptionParser(version="0.1beta")
	parser.add_option("-c","--command",dest="cmd")
	parser.add_option("-f","--filename",dest="filename")
(options, args) = parser.parse_args()
#print 'options: %s, args: %s' % (options, args)
ssh_do = ssh_cmd(options.filename,options.cmd)
#print 'ssh_do returned %s' % ssh_do.ssh_login_do()
ssh_do.ssh_login_do()
sys.exit
