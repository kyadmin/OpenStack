#!/usr/bin/python
#_*_ coding:UTF-8 _*_

import sys,os
reload(sys)
sys.setdefaultencoding('utf8')
import ConfigParser

class tenant_conf:
	def __init__(self,filename):
		self.filename = filename
		self.config = ConfigParser.ConfigParser()
		self.config.read(self.filename)
		self.config.sections()
	def tenant_name(self):
		return self.config.sections()
	def tenant_rescoure(self):
		s=self.config.sections()
		import time
		rescoure = []
		for i in s:
			 c=self.config.items(i)
		         rescoure.extend(c)
		return rescoure
		

			
