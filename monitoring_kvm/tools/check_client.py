import os,sys
import time

check_file = '/root/script/monitoring_kvm/tools/check_client_conn'
if not os.path.exists(check_file):
        os.mknod(check_file,0o755)

filename='monitoring_kvm.conf'

def client():
	with open(check_file) as f:
		a = f.readlines()
	return a	
		
