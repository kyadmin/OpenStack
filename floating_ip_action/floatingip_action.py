#G!/usr/bin/python
#_*_ coding: UTF-8 _*_
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import conf
import shell_cmd as shell
import time
import threading
import Queue

def  shell_cmd(camd):
	subprocess.PIPE
	#cmd= 'ping -c %s -i %s %s' % (3,0.01, "172.16.205."+str(i)+"\n")
	P=subprocess.Popen(cmd,stdin = subprocess.PIPE,
                     stdout = subprocess.PIPE,
                     stderr = subprocess.PIPE,
                     shell = True)
	P.stdin.close()
	P.wait()
	return  P.stdout.readlines()
cf = conf.conf('floatingip.conf')

def external:
    cmd = 'neutron net-list --router:external=True'

def floatingip_create(user,num):
        count = 1
        while (count < num+1):
                cmd_neutron = 'neutron floatingip-create %s' % (external)
                neutrn = shell.shell_cmd(cmd_neutron)
                if (user == 'admin'):
                        shell.shell_cmd('bash')
                        rc = cf.admin_rc()
                        cmd_source = 'source %s' %(rc)
                        source = shell.shell_cmd(cmd_source)
                        cmd_neutron
                        shell.shell_cmd('exit')
                        print "hello,word" 
                        count = count + 1
                elif(user == 'kycloud'):
                    pass
                
                elif(user == 'kyprivate'):
                    pass
                    
                elif(user == 'kyp2p'):
                    pass
                
                else:
                        print "请输入正确的user"
                
    
