#!/usr/bin/env python
# coding=utf-8
import time

__author__ = 'hansz'

import threading
import Queue
import sys
import urllib2
import json
# 定义一个线程池管理器类，用于启动 停用管理线程池。
class Threading_pools(object):

    def __init__(self,threads_num = 10):
        # 初始化工作队列结果队列
        self.work_queue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.threads = []
        self.start_thread_pool(threads_num)
    def start_thread_pool(self,threads_num):
        for i in range(threads_num):
            thread = Work_Thread(self.work_queue,self.result_queue)
            self.threads.append(thread)

    def append_job(self,func,args):
        self.work_queue.put((func,args))

    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()


# 工作线程，线程池中的线程
class Work_Thread(threading.Thread):
    def __init__(self,work_queue,result_Queue,poll_timeout = 5,**kwargs):
        threading.Thread.__init__(self,kwargs=kwargs)
        self.setDaemon(True)
        self.work_queue = work_queue
        self.resultQueue = result_Queue
        self.polltimeout = poll_timeout
        self.start()

    def run(self):
        while True:
            try:
                call,args= self.work_queue.get(timeout = self.polltimeout)
                res = call(args)
                res = str(res)
                self.resultQueue.put(res+" | "+self.getName())
            except Queue.Empty:
                break
            except :
                print sys.exc_info()
                raise

