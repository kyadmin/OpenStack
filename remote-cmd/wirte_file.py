#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import time
import sys
import traceback
import os
import socket
from otomat.conf import conf
from threading import *
#
class recive_report:
        def __init__(self,report_file = "report",filename = "otomat.cnf"):
            self.filename = filename
            cnf = conf.files_conf_check(self.filename)
            self.path = cnf.server_report_path()
            print self.path
            self.report = report_file
            print self.report
        def report(self,data):
            print self.path
            print self.report
            os.chdir(self.path)
            f = open(self.report,'w+')
            try:
                f.write(data)
            except IOError:
                traceback.print_exc()
            finally:
                f.close()
if __name__ == "__main__":
    t = recive_report()
    t.report()
