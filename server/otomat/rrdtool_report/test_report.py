#!/usr/bin/python
import report
import time
#
t = report.graph_rrdtool('/etc/otomat/otomat.cnf')
t.rrdb()
while True:
	t.rrdb_update()
	time.sleep(300)
	continue
