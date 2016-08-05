#_*_ coding: UTF-8 _*_
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import  ConfigParser
class files_conf:
        def __init__(self,filename):
                self.filename = filename


        def base_operate(self):
                # 生产config 对象
                conf = ConfigParser.ConfigParser()
                # 用config对象读取配置文件
                conf.read(self.filename)
                # 以列表的形式返回section
                s = conf.sections()
                # 得到指定的sections, options
                # address
                o_address = conf.get("host_address","host")
		#print o_address
                user_list = o_address.split(',')
                for i in user_list:
                        print i
                # user
                o_user =  conf.get("host_user","user_root")
		print o_user
                # password
                o_password = conf.get("host_password","password")
		print o_password
		return o_address,o_user,o_password
#if __name__=='__main__':
#	p=files_conf('controller_list.ini')
#	p.base_operate()
		
if __name__ == "__main__":
	from optparse import OptionParser
	parser = OptionParser(version="0.1beta")
	parser.add_option("-f","--filename",dest="filename",
			default="controller_list.ini",
			metavar="FILENAME")
	(options,args) = parser.parse_args()
	#print 'options: %s, args: %s' % (options,args)
	p = files_conf(options.filename)
	print  p.base_operate()
