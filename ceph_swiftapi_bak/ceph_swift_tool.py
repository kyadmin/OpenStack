# !/usr/bin/env python
# --*-- coding:utf-8 -*-
#  Author: Andre Yang
#  Email: wangyouyan2146@gmail.com
#  File Name: ceph_swift_tool
#  Description:
#  Edit History: 2015-12-16
# ==================================================
import sys
try:
    import swiftclient
except:
    print("loading swiftclient mode failed, process will exit....")
    sys.exit(1)

def action_ceph_do(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        tmp = func(*args,**kwargs)
        user = tmp[0]
        key = tmp[1]
        authurl = tmp[2]
        try:
            conn = swiftclient.Connection(
                user=user,
                key=key,
                authurl=authurl,
            )
            print("connection %s success...." % authurl)
            def create_container(container_name):
                try:
                    # create a container
                    conn.put_container(container_name)
                    print("Container %s to create success...." % container_name)
                except:
                    print("Container %s to create failed...." % container_name)
            def create_object(object_name,container_name):
                try:
                    with open(object_name,'r') as f:
                        conn.put_object(container_name,object_name,
                                        contents=f.read())
                                        #content_type='text/plain')
                    print("Object %s to create success...." % object_name)
                except:
                    print("Object %s to create failed...." % object_name)
            def list_continers():
                try:
                    for container in conn.get_account()[1]:
                        print container['name']
                except:
                    print("Container list failed.....")
            def show_container_content(container_name):
                try:
                    for data in conn.get_container(container_name)[1]:
                        print '{0}\t{1}\t{2}'.format(data['name'],data['bytes'],data['last_modified'])
                except:
                    print("show %s container failed..." % container_name)
            def download_object(object_name,container_name):
                try:
                    obj_tupe = conn.get_object(container_name,object_name)
                    with open(object_name,'wb') as f:
                        f.writelines(obj_tupe[1])
                    print("Download %s success...." % object_name)
                except:
                    print("Download %s failed...." % object_name)
            def delete_object(container_name,object_name):
                try:
                    conn.delete_object(container_name,object_name)
                    print("Delete %s success..." % object_name)
                except:
                    print("Delete %s failed..." % object_name)
            def delete_container(container_name):
                try:
                    conn.delete_container(container_name)
                    print("Delete %s success..." % container_name)
                except:
                    print("Delete %s failed..." % container_name)
        except:
            print("connection %s faild ....." % authurl)
        return tmp
    return wrapper


class ceph:
    def __init__(self,container_name,object_name):
        self.user = 'test:swift'
        self.key = '3YAbLcxCLLQpEsChAIYDepBUTq3y006K43aYmGem'
        self.authurl = 'http://172.16.209.81/auth/1.0'
        self.action = None
        self.container_name = container_name
        self.object_name = object_name

    @action_ceph_do
    def create_container(self.user,self.key,self.authurl,
                                  self.container_name,self.object_name=None,
                                  self.action="create_container"):
        return (sel.user,self.key,self.authurl,self.container_name,
                self.object_name,self.action)
    @action_ceph_do
    def create_object(self.user,self.key,self.authurl,self.container_name,
                                self.object_name,self.action = "create_object"):
        return (self.user,self.key,self.authurl,self.container_name,
                self.object_name,self.action)
    @action_ceph_do
    def list_containers(self.user,self.key,self.authurl,
                                    self.container_name,self.object_name,
                                    self.action="list_containers"):
        return (self.user,self.key,self.authurl,self.container_name,
                self.object_name,self.action)
    @action_ceph_do
    def show_container_content(self.user,self.key,self.authurl,self.container_name,
                                        self.object_name=None,
                                        self.action="show_container_content"):
        return (self.user,self.key,self.authurl,self.container_name,
               self.object_name,self.action)
    @action_ceph_do
    def download_object(self.user,self.key,self.authurl,self.container_name,
                                  self.object_name,self.action="downlaod_object"):
        return (self.user,self.key,self.authurl,self.container_name,self.object_name,self.action)
    @action_ceph_do
    def  delete_object(self.user,self.key,self.authurl,self.container_name,
                            self.object_name,self.action="delete_object"):
        return (self.user,self.key,self.authurl,self.container_name,
               self.object_name,self.action)
    @action_ceph_do
    def delete_container(self.user,self.key,self.authurl,self.container_name,
                             self.object_name=None,self.action="delete_container"):
        return (self.user,self.key,self.authurl,self.container_name,
                self.object_name,self.action)
def usage():
    usages='''
precondition:
    configure user,key,authurl for ceph_swift_tool;
    example:
    def __init__(self):
        self.user = 'test:swift'
        self.key = '3YAbLcxCLLQpEsChAIYDepBUTq3y006K43aYmGem'
        self.authurl = 'http://monosd01/auth/1.0'
Usage:
    python ceph_swift_tool.py [option <create|upload|delete|list|download>] [contianer <contianer name>] [object <object name>]
Example:
    # create contianer
    python ceph_swift_tool.py  create kycloud
    # list  contianer
    python ceph_swift_tool.py  list
    # delete an contianer
    python ceph_swift_tool.py  delete kycloud
    # upload object in kycloud contianer
    python ceph_swift_tool.py  create|upload kycloud kycloud_file
    # list a container's content
    python ceph_swift_tool.py  list kycloud
    # download an object
    python ceph_swift_tool.py  download kycloud kycloud_file
    # delete an object
    python ceph_swift_tool.py  delete kycloud
    '''
    print usages

if __name__ == '__main__':
    if len(sys.argv) == 3:
        container_cmd = sys.argv[2]
        print container_cmd
        pass
    elif len(sys.argv) == 4:
        object_cmd = sys.argv[3]
        print object_cmd
        pass
    elif len(sys.argv) == 2:
        option = sys.argv[1]
        print option
        if option == '-v' or option == '--version':
            print('0.1 beta')
        else:
            usage()

    else:
        usage()


