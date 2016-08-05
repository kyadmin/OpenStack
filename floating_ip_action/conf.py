#_*_ coding: UTF-8 _*_
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import  ConfigParser

class conf:
        def __init__(self,filename):
                self.filename = filename
                self.conf = ConfigParser.ConfigParser()
                self.conf.read(self.filename)
                s = self.conf.sections()
	# server configure
        def admin_rc(self):
                rc = self.conf.get("env","admin")
                return rc
        def kycloud_rc(self):
                rc = self.conf.get("env","kycloud")
                return rc
        def kyprivate_rc(self):
                rc = self.conf.get("env","kyprivate")
                return rc
        def kyp2p(self):
                rc = self.conf.get("env","kyp2p")
                return rc
