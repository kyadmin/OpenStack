#_*_ encoding: UTF-8 _*_
import ConfigParser
def base_operate():
                # 生产config 对象
                conf = ConfigParser.ConfigParser()
                # 用config对象读取配置文件
                conf.read('controller_list.ini')
                # 以列表的形式返回section
                s = conf.sections()
                # 得到指定的sections, options
                # address
                o_address = conf.get("host_address","host")
                print o_address
                user_list = o_address.split(',')
                for i in user_list:
                        print i
                # user
                o_user =  conf.get("host_user","user_root")
                print o_user
                # password
                o_password = conf.get("host_password","password")
                print o_password

base_operate()

