#_*_ coding: UTF-8 _*_
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import  ConfigParser
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
if __name__=='__main__':
	p=files_conf('controller_list.ini')
	print "username: %s" % p.username()
	r = list(p.address().split(','))
	for j in r:
		print  "address: %s" % j
	print "password: %s" %p.password()
		
