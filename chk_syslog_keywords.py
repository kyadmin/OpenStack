#!/usr/bin/env python
#_*_ coding: utf-8 _*_

import os,re

p = re.compile(r"root|ROOT")
 
for f in open("/tmp/syslog"):
    S = p.search(f)
    try:
        if S:
            print S.group(0)
    except:
        print "pipeishibai"

if __name__ == '__main__':
    re_grep()
