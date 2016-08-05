# !/usr/bin/env python
# --*-- coding:utf-8 -*-
#  Author: Andre Yang
#  Email: wangyouyan2146@gmail.com
#  File Name:
#  Description:
#  Edit History:
# ==================================================

def w1(func):
    def inner(arg):
        #验证1
        #验证2
        #验证3
        return func(arg)
    return inner

@w1
def f1(arg):
    print arg

@w1
def f2(arg):
    print arg

@w1
def f3(arg):
    print arg

@w1
def f4(arg):
    print arg
if __name__ == '__main__':
    f1('f1')
    f2('f2')
    f3('f3')
    f4('f4')