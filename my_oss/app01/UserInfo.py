#_*_coding:utf-8_*_
import paramiko

host_name='172.16.201.36'
host_username='root'
host_password='OpenStack2016!@#$'
host_port=22
radosgw_port=8080



class paramiko_cmd(object):
    def __init__(self,host_name=host_name,host_username=host_username,host_password=host_password,host_port=22,radosgw_port=radosgw_port):
        self.host_name=host_name
        self.host_username=host_username
        self.host_password=host_password
        self.host_port=host_port
        self.radosgw_port=radosgw_port
        self.conn=paramiko.SSHClient()
        self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.conn.connect(hostname=host_name,port=host_port,username=host_username,password=host_password)

    def user_info_get(self,username):
        access_key_cmd = r"radosgw-admin user info --uid=%s |grep -A 2 '%s\"\,$' |grep access_key |awk '{print $NF}' |cut -d',' -f1|cut -d\" -f2" % (username,username)
        secret_key_cmd = r"radosgw-admin user info --uid=%s |grep -A 2 '%s\"\,$' |grep secret_key |awk '{print $NF}'|cut -d\" -f2" %  (username,username)
        stdin, stdout, stderr = self.conn.exec_command(access_key_cmd)
        s3_access_key = stdout.read().strip()
        stdin, stdout, stderr = self.conn.exec_command(secret_key_cmd)
        s3_secret_key = stdout.read().strip()
        self.conn.close()
        user_info=UserInfo(username,s3_access_key,s3_secret_key,self.host_name,self.radosgw_port)
        return user_info

class UserInfo(object):
    def __init__(self,username,s3_access_key,s3_secret_key,radosgw_host,radosgw_port=7480,swift_access_key='',swift_secret_key='',display_name='',email=''):
        self.username=username
        self.s3_access_key=s3_access_key
        self.s3_secret_key=s3_secret_key
        self.radosgw_host=radosgw_host
        self.radosgw_port=radosgw_port
        self.swift_secret_key=swift_access_key
        self.swfit_secret_key=swift_access_key
        self.display_name=display_name
        self.email=email
    def tell_user_info(self):
        print "Username:%s S3_ACCESS_KEY:%s S3_SECRET_KEY:%s" %(self.username,self.s3_access_key,self.s3_secret_key)


if __name__ == '__main__':
    username='linhaifeng'

    test=paramiko_cmd(host_name,host_username,host_password,host_port)
    user_info=test.user_info_get(username)
    user_info.tell_user_info()
