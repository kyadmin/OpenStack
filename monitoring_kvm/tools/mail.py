#!/usr/bin/python
#
#========================================================================
# Author:Andre
# Email:wangyouyan2146@gmail.com
# File Name: 
# Description:
# Edit History:
# 2015-09-23 File created.
#========================================================================
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time

from tools import log as logging
from tools import shell_cmd as shell

def today_time():
	n = time.localtime(time.time())
	if n.tm_mon < 10 and n.tm_mday <10:
		today = str(n.tm_year)+'-0'+str(n.tm_mon)+'-0'+str(n.tm_mday)+' '+str(n.tm_hour)+':'+str(n.tm_min)+':'+str(n.tm_sec)
	elif n.tm_mon < 10 and n.tm_mday >= 10:
		today = str(n.tm_year)+'-0'+str(n.tm_mon)+'-'+str(n.tm_mday)+' '+str(n.tm_hour)+':'+str(n.tm_min)+':'+str(n.tm_sec)
	elif n.tm_mon >= 10 and n.tm_mday <10:
		today = str(n.tm_year)+'-'+str(n.tm_mon)+'-0'+str(n.tm_mday)+' '+str(n.tm_hour)+':'+str(n.tm_min)+':'+str(n.tm_sec)
	elif n.tm_mon >= 10 and n.tm_mday <10:
		today = str(n.tm_year)+'-'+str(n.tm_mon)+'-0'+str(n.tm_mday)+' '+str(n.tm_hour)+':'+str(n.tm_min)+':'+str(n.tm_sec)
	return today
times = today_time()

def mail_content(times,host,action):
	content = """
  You will %s switching host,as a result to %s switch %s.
Greethings from ShiJiazhuang!!!
""" % (times,host,action)
	return content

class send_mail:
	def __init__(self,mailbox):
		self.mailbox = mailbox
		self.title = "[Cloud] %s The host switch" % today_time()
	def send_success(self,host):
		title = self.title
		mail_cmd = '/bin/mail -s %s  %s < %s' % (title,self.mailbox,mail_content(times,host,'successfully'))
		shell.shell_cmd(mail_cmd) 
		return 0
	def send_faild(self,host):
		title = self.title
                mail_cmd = '/bin/mail -s %s %s  < %s' % (title,self,mailbox,mail_content(times,host,'Faild.'))
                shell.shell_cmd(mail_cmd) 
                return 1

