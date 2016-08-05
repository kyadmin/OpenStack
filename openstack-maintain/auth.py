#!/usr/bin/env python
# coding=utf-8
# created by hansz
import keystoneclient.v2_0.client as ksclient

class KeyStone(object):
    def __init__(self,auth_url,username,password,tenant_name):
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.tenant_name = tenant_name
        self.keystone = ksclient.Client(auth_url=self.auth_url,
                           username=self.username,
                           password=self.password,
                           tenant_name=self.tenant_name)

        self.token = self.keystone.auth_token

    def get_token(self):
        return self.token

    def get_keystone_creds(self):
        d = {}
        d['username'] = self.username
        d['password'] = self.password
        d['auth_url'] = self.auth_url
        d['tenant_name'] = self.tenant_name
        return d

    @property
    def get_nova_creds(self):
        d = {}
        d['username'] = self.username
        d['api_key'] =self.password
        d['auth_url'] = self.auth_url
        d['project_id'] = self.tenant_name
        return d


if __name__ == "__main__":
    # auth_url = "http://172.16.209.11:35357/v2.0"
    # username = "kycloud"
    # password = "che001"
    # tenant_name = "kycloud"
    # k1 = KeyStone(auth_url,username,password,tenant_name)

    auth_url = "http://172.16.209.11:35357/v2.0"
    username = "admin"
    password = "che001"
    tenant_name = "admin"
    k = ksclient.Client(auth_url=auth_url,username=username,password=password,tenant_name=tenant_name)
    # k1 = KeyStone(auth_url, username, password, tenant_name)
    print dir(k)
    print dir(k.tenants)
    print k.tenants.list()
    for i in k.tenants.list():
        print dir(i)
        print i.name
        users =  i.list_users()
        for user in users:
            print dir(user)
            print user.name
            print user.id
            print user._info
            print
            # print dir(i.get)
    # print dir(ksclient.users.UserManager.get())

