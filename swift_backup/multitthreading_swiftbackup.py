import os,time
import httplib
import json
from hashlib import md5
from urlparse import urlparse,urlunparse,urljoin
from urllib import quote
from eventlet.green.httplib import HTTPConnection
#from threading import *
from threadpool import *

global now,n
n = time.localtime(time.time())
now = str(n.tm_year)+'-0'+str(n.tm_mon)+'-'+str(n.tm_mday)

def read_file(fpath):
	with  open(fpath) as f:
	        for i in f.readlines():
		        yield i


def http_connection(url):
	'''
	test http_connection
	'''
	parsed = urlparse(url)
	conn = HTTPConnection(parsed.netloc)
	return parsed, conn

def json_request(method, url, **kwargs):
	kwargs.setdefault('headers', {})
	kwargs['headers']['Content-Type'] = 'application/json'
	kwargs['body'] = json.dumps(kwargs['body'])
	parsed, conn = http_connection(url)
	conn.request(method, parsed.path, **kwargs)
	resp = conn.getresponse()
	body = resp.read()
	body = json.loads(body)
	return resp, body

def get_auth():
	url = 'http://10.10.0.200:5000/v2.0/'
	body = {'auth': {'passwordCredentials': {'password': 'swift',
	'username':'swift'},'tenantName': 'services'}}
	token_url = urljoin(url, "tokens") 
	resp, body = json_request("POST", token_url, body=body)
	token_id = None
	try:
		url = None
		catalogs = body['access']["serviceCatalog"]
		for service in catalogs:
			if service['type'] == 'object-store':
				url = service['endpoints'][0]['publicURL']
		token_id = body['access']['token']['id']
	except(KeyError,IndexError):
		print 'Error'
	return url, token_id

def get_object(L):
        ####
        global now
        ### 
        PWD = os.getcwd()+'/'
        backup_dir = 'data_backup/'
        url, token = get_auth()
        parsed, conn = http_connection(url)
	#path = '%s/%s/%s' % (parsed.path, quote('test'), quote('rdo-release-havana-8.repo'))
	#path = '%s/%s/%s' % (parsed.path, quote('andre-test'), quote('repo/zatree/zabbix-2.2.x/README_UTF.md'))
        #print "This is ################## :%s" %i
	path = '%s/%s/%s' % (parsed.path, quote('andre-test'), quote(L))
        method = 'GET'
        headers = {'X-Auth-Token': token}
	conn.request(method, path,'',headers)
	resp = conn.getresponse()
	body = resp.read()
	#body =  resp.fp()
	#print "This is body:%s" % body
	#print "This is path: %s" % path
        #print "############ :%s" %L
        #print "This is resp status: %s" % resp.status
        if resp.status < 200 or resp.status >= 300:
                body = resp.read()
                print body
        ###############################
        a = L.split('/')
        #print "###This is a##%s" %a
        delimiter = '/'
        mylist = []
        for x in range(int(len(a))-1):
                mylist.append(a[x])
        #print  delimiter.join(mylist)
        if '/' in L:
                file_path = PWD + backup_dir + delimiter.join(mylist)
                out_file = a[int(len(a))-1]
                #print "###This is Outfile###%s" %out_file
                if not os.path.exists(file_path):
                        os.makedirs(file_path,0o755)
                os.chdir(file_path)
        else:
                out_file = L
                os.chdir(backup_dir)
                        
        #out_file = "rdo-release-havana-8.repo"
        #print "#####%s" %out_file
        if out_file  != '_':
                filename = out_file.split('\n')[0]
                #print "This is dir:%s" % backup_dir    
                try:
                        fp = open(filename,'rb')
                        #fp = open(filename,'wb')
                        #fp.writelines(body)
                        #fp.close()
                except IOError:
                        pass
                else:
                        with fp:
                                md5sum = md5()
                                while True:
                                        data = fp.read(65536)
                                        if not data:
                                                break
                                        md5sum.update(data)
                try:
                        fp = open(filename,'wb')
                        fp.writelines(body)
                        print "File %s download success!" %fp
                        time.sleep(0.01)
                finally:
                        fp.close()
                os.chdir(PWD)
            
def pool_list():
        global now
        List = []
        for i in read_file('swift_list-'+now):
                List.append(i.split('\n')[0])
        return List
                

                
        


if __name__ == "__main__":
        L = pool_list()
        #print L
        pool = ThreadPool(1000)
        requests = makeRequests(get_object,L)
        for req in requests:  
                pool.putRequest(req) 
        pool.wait()
	#get_object()
	'''
	MaxThread = 1000
	sem = BoundedSemaphore(MaxThread)
	for a in range(10000):
		sem.acquire()
		Thread(target=printthread(a),args=(a,)).start()
	print "All thread has create,Wait for thread exit."

	for a in range(MaxThread):
		sem.acquire()

	print  "All thread exit"
	'''
