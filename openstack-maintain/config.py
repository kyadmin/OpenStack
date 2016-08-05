#!/usr/bin/env python
# coding=utf-8
# created by hansz

import auth



# auth_url = "http://172.16.209.11:35357/v2.0"
# auth_url ="http://10.10.0.200:5000/v2.0/"
# username = "hansz"
# password = "hansz"
# tenant_name = "hansz_test"
# k1 = auth.KeyStone(auth_url,username,password,tenant_name)
#

tenant_user_list = [
#    {
#    "auth_url": "http://10.10.0.200:5000/v2.0/",
#    "username": "hansz",
#    "password": "hansz",
#    "tenant_name": "hansz_test",
#    },
#    {
#    "auth_url": "http://10.10.0.200:5000/v2.0/",
#    "username": "lhf_test",
#    "password": "lhf123",
#    "tenant_name": "lhf_test",
#    },

]
tenant_list = [
	 "hansz_test",
#	 	"Che001","dbswift","kychekk",
#		"kycloudstaging",
#		 "kypaybackend","kysso","KY_DBA",
#		"KY_DevOps","KY_Dianfubao","KY_P2P","KY_Platform",
#		"KY_Qingyidai",
#		"performance","Ultimate-Backend",
#		"Ultimate-Kypay","Ultimate-Qingyidai","Ultimate-SSO"	

]
#tenant_list=["hansz_test","lhf_test"]
for i in tenant_list:
    template = {
    		"auth_url": "http://10.10.0.200:5000/v2.0/",
    		"username": "hansz",
    		"password": "hansz",
    		"tenant_name": i,
    	}
    tenant_user_list.append(template)

user_creds_list = []
for i in tenant_user_list:
    # print i
    k1 = auth.KeyStone(i["auth_url"], i["username"], i["password"], i["tenant_name"])
    # print k1.get_nova_creds
    user_creds_list.append(k1.get_nova_creds)
    # print dir(my_nova)
#     # my_nova.operator(creds=k1.get_nova_creds)
print user_creds_list

