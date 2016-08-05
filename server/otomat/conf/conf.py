#_*_ coding: UTF-8 _*_
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import  ConfigParser
class files_conf_ssh:
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

class files_conf_check:
        def __init__(self,filename):
                self.filename = filename
                self.conf = ConfigParser.ConfigParser()
                self.conf.read(self.filename)
                s = self.conf.sections()
	# server configure
        def server_port(self):
                s_port = self.conf.get("server","port")
                return s_port
        def server_host(self):
                s_host = self.conf.get("server","host")
                return s_host
        def server_ip(self):
                s_ip = self.conf.get("server","my_ip")
                return s_ip
        def server_path(self):
                s_path = self.conf.get("server","report_path")
                return s_path
        def server_worker(self):
                s_worker = self.conf.get("server","worker")
                return s_worker
        def server_log(self):
                s_log = self.conf.get("server","server_log")
                return s_log
        def report_log(self):
                r_log = self.conf.get("server","report_log")
                return r_log
        def email_log(self):
                e_log = self.conf.get("server","email_log")
                return e_log
        def server_logdir(self):
                s_logdir = self.conf.get("server","log_dir")
                return s_logdir
        #  mysql database  configure
	def sql_host(self):
                sql_host = self.conf.get("sql","host")
                return sql_host
        def sql_user(self):
                sql_user = self.conf.get("sql","user")
                return sql_user
        def sql_password(self):
                sql_password = self.conf.get("sql","password")
                return sql_password
        def sql_defaultdb(self):
                sql_db = self.conf.get("sql","defaultdb")
                return sql_db
	# rrdtool configure
        def rrdtool_host(self):
                rrdtool_host = self.conf.get("rrdtool","host")
                return rrdtool_host
        def rrdtool_cpu(self):
                rrdtool_cpu  = self.conf.get("rrdtool","cpu")
                return rrdtool_cpu
        def rrdtool_mem(self):
               	rrdtool_mem  = self.conf.get("rrdtool","mem")
                return rrdtool_mem
        def rrdtool_disk(self):
                rrdtool_disk = self.conf.get("rrdtool","disk")
                return rrdtool_disk
        def rrdtool_nic(self):
                rrdtool_nic = self.conf.get("rrdtool","network")
                return rrdtool_nic
	# graph configure
        def graph_cpu(self):
                graph_cpu = self.conf.get("graph","cpu")
                return graph_cpu
        def graph_mem(self):
                graph_mem = self.conf.get("graph","mem")
                return graph_mem
        def graph_disk(self):
                graph_disk = self.conf.get("graph","disk")
                return graph_disk
        def graph_network(self):
                graph_network = self.conf.get("graph","network")
                return graph_network
	# cleint agent configure
        def client_ip(self):
                c_ip = self.conf.get("client","my_ip")
                return c_ip
        def client_host(self):
                c_host = self.conf.get("client","host")
                return c_host
        def client_port(self):
                c_port = self.conf.get("client","port")
                return c_port
        def  nic_port(self):
                n_port = self.conf.get("client","nic")
                return n_port
        def client_log(self):
                c_log = self.conf.get("client","log")
                return c_log
        def client_logdir(self):
                c_logdir = self.conf.get("client","log_dir")
                return c_logdir
