# !/usr/bin/env python
# --*-- coding:utf-8 -*-
#  Author: Andre Yang
#  Email: wangyouyan2146@gmail.com
#  File Name:
#  Description:
#  Edit History:
# ==================================================
import sys
sys.path.append('~/repo/Python_Projects/django_prodject/mysite/webapp')
import wrapper

print('---------')
ret_list = wrapper.fetch_server_list('test')
print ret_list

