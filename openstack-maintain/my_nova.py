#!/usr/bin/env python
# coding=utf-8
# created by hansz
import os
import random
import threading_pool
import novaclient.client as nvclient
import cinderclient.client as cinclient
import threading

import shutil

import config, log_record
import sys, time
import pickle
import multiprocessing

reload(sys)
sys.setdefaultencoding("utf-8")

creds = config.k1.get_nova_creds

# 定义nova类，用来获取云主机信息，操作云主机
class Nova(object):
    def __init__(self, version, cinder1, **kwargs):
        self.version = version
        self.kwargs = kwargs
        self.nova = nvclient.Client(version, **kwargs)
        self.cinder1 = cinder1

    # 获取云主机列表
    def get_server_list(self):
        return self.nova.servers.list()

    # 通过id获取云主机对象
    def get_server(self, server_id):
        self.server_list = self.nova.servers.list()
        for server_obj in self.server_list:
            if server_obj.id == server_id:
                return server_obj
    # 通过id启动云主机
    def start_server(self, server_id):
        server = self.get_server(server_id)
        try:
            server.start()
            start_time = time.clock()

            print u"\n%s 启动成功" % server.name
        except Exception as e:
            log_record.error_logging(u"server%s 启动失败%s" % (server_id, e))
            return False
    # 通过id关闭云主机
    def stop_server(self, server_id):
        server = self.get_server(server_id)
        try:
            server.stop()
            start_time = time.clock()
            while self.get_server_status(server_id) == ("ACTIVE" or "Active"):
                run_time = time.clock() - start_time
                if run_time > 20:
                    log_record.error_logging(u"Timeout 20s .%s" % server_id)
                else:
                    print "%s" % (u"正在关闭%s  " % server.name)
                    print self.get_server_status(server_id)
            print u" \n%s 关闭成功" % server.name
        except Exception as e:
            log_record.error_logging(u"server %s 关闭失败%s" % (server_id, e))
            return False

    # 根据id获取云主机的状态
    def get_server_status(self, server_id):
        server = self.get_server(server_id)
        status = server.status
        return status

    # 通过云主机id和volume的id卸载volume
    def detach_volume(self, server_id, volume_id):
        try:
            self.nova.volumes.delete_server_volume(server_id, volume_id)
            print u"卸载云盘 %s " % volume_id, self.cinder1.volume_status(volume_id)
            while self.cinder1.volume_status(volume_id) == ("In-Use" or "in-use" or "detaching"):
                print u"正在卸载%s  " % volume_id
                time.sleep(1)
            print u'\n%s卸载成功' % volume_id
            return True
        except Exception as e:
            print u'卸载云盘失败%s' % volume_id, e
            # time.sleep(5)
            volume_status = self.cinder1.volume_status(volume_id)
            if volume_status == "in-use":
                pass
                # self.detach_volume(server_id,volume_id)
            else:
                print "actually success"
                return True
            return False

    # 通过云主机的id和volume的id挂载volume
    def attach_volume(self, server_id, volume_id, device, index):
        try:
            # print index
            # while index==0 and  len(self.nova.volumes.get_server_volumes(server_id))!=0:
            # 卸载关机之后,volume的信息可能不会立即同步，需要等一会。
            # print "waiting volume info update ."

            self.nova.volumes.create_server_volume(server_id, volume_id, device)
            print u'挂载云盘%s' % volume_id, self.cinder1.volume_status(volume_id)
            start = time.clock()
            while self.cinder1.volume_status(volume_id) != ("in-use" or "In-Use"):
                sys.stdout.write("\rattaching %s" % (random.randint(1, 10) * "."))
                end_time = time.clock()
                if end_time - start > 2:
                    print u"挂载超时,跳过"
                    break
            print u"挂载成功"
            return True
        except Exception as e:
            print u'挂载%s失败' % volume_id, e
            if self.cinder1.volume_status(volume_id) == "in-use":
                return True
            else:
                pass
            return False


class Cinder(object):
    def __init__(self, version, **kwargs):
        self.cinder = cinclient.Client(version, **kwargs)
        self.volumes = self.cinder.volumes
        self.volume_list = self.volumes.list()
        # print self.volume_list

    # 获取volume对象
    def get_volume(self, volume_id=None):
        for volume in self.volume_list:
            if volume_id == volume.id:
                return volume

    # 获取volume信息,按照主机组。
    def get_attachments(self):
        # attachments = {serverid: [attachvolume2,attachvolume2],}
        all_server_attachments = {}
        # print self.volume_list,"volume_list"
        for volume in self.volume_list:
            if len(volume.attachments) == 0: continue
            volume_info = volume.attachments[0]
            # print volume_info,"volume_info"
            # print volume_info["server_id"]
            if volume_info[u"server_id"] not in all_server_attachments.keys():
                #     如果之前没有这个主机
                all_server_attachments[volume_info["server_id"]] = []
            all_server_attachments[volume_info["server_id"]].append(volume_info)
            # print "all",all_server_attachments
        return all_server_attachments

    # 获取volume状态
    def volume_status(self, volume_id):
        # status 要实时的，所以要重新获取一遍值
        self.volumes = self.cinder.volumes
        self.volume_list = self.volumes.list()

        for volume in self.volume_list:
            if volume_id == volume.id:
                return volume.status

# 定义关机规则，有云盘卸载云盘，没有就直接关机
def stop_vm(server, server_cinder_info, nova1, cinder1):
    break_status = False
    server_status = nova1.get_server_status(server.id)
    print u"server_host name is %s , id is %s " % (server.name, server.id)

    if server_cinder_info == [] or server.id not in server_cinder_info.keys():
        #     该租户没有挂载过云盘 直接重启
        print  u"%s该主机没有挂载云盘，直接关机" % server.name
        if server_status == u"SHUTOFF":
            # nova1.start_server(server.id)
            break_status = True
        else:
            nova1.stop_server(server.id)
            # nova1.start_server(server.id)
            break_status = True
    if break_status: exit("error ")
    server_volume = server_cinder_info[server.id]
    for volume in server_volume:
        #     卸载云盘
        detach_status = nova1.detach_volume(server.id, volume["volume_id"])
        if not detach_status:
            log_record.error_logging(u"云盘卸载失败,跳过此机器重启,请查看日志%s" % (server.id))
            break_status = True

    # if break_status: exit("error ")

    # 关机
    if server_status != u"SHUTOFF":
        nova1.stop_server(server.id)


def start_vm(server, server_cinder_info, nova1, cinder1):
    # def start_vm(args):
    #   server,server_cinder_info,nova1,cinder1=args
    # 挂载云盘

    break_status = False
    server_status = nova1.get_server_status(server.id)
    if server_cinder_info == [] or server.id not in server_cinder_info.keys():
        # if True:
        #     该租户没有挂载过云盘 直接启动
        print  u"%s该主机没有挂载云盘，直接启动" % server.name
        if server_status == u"SHUTOFF":
            nova1.start_server(server.id)
            break_status = True
        else:
            break_status = True

    else:
        server_volume = server_cinder_info[server.id]
        # time.sleep(random.random())
        for index, volume in enumerate(server_volume):
            # cinder1.attach_volume(volume["server_id"], volume["device"], volume["volume_id"])
            if cinder1.volume_status(volume["volume_id"]) == "in-use":
                print u"云盘已经挂载，异常,直接启动%s" % server_status
                if server_status == u"SHUTOFF":
                    nova1.start_server(server.id)
                break
            # print cinder1.volume_status(volume["volume_id"])

            attach_status = nova1.attach_volume(volume["server_id"], volume["volume_id"], volume["device"], index)
            if not attach_status:
                print u"云盘挂载失败,跳过此机器启动,请查看日志"
                # print cinder1.volume_status(volume["volume_id"])
        # 开机
        nova1.start_server(server.id)




# 卸载所有的盘
def detach_vm(server,server_cinder_info,nova1,cinder1):
    break_status = False
    print u"server_host name is %s , id is %s " % (server.name, server.id)

    if server_cinder_info == [] or server.id not in server_cinder_info.keys():
        #     该租户没有挂载过云盘 直接重启
        print  u"%s该主机没有挂载云盘," % server.name
        break_status = True
    if break_status: exit("error ")
    server_volume = server_cinder_info[server.id]
    for volume in server_volume:
        #     卸载云盘
        detach_status = nova1.detach_volume(server.id, volume["volume_id"])
        if not detach_status:
            log_record.error_logging(u"云盘卸载失败,跳过此机器重启,请查看日志%s" % (server.id))

# 挂载所有的盘
def attach_vm(server,server_cinder_info,nova1,cinder1):
    # 挂载云盘
    server_status = nova1.get_server_status(server.id)
    if server_cinder_info == [] or server.id not in server_cinder_info.keys():
        pass
    else:
        server_volume = server_cinder_info[server.id]
        for index, volume in enumerate(server_volume):
            if cinder1.volume_status(volume["volume_id"]) == "in-use":
                print u"云盘已经挂载，"
            attach_status = nova1.attach_volume(volume["server_id"], volume["volume_id"], volume["device"], index)
            if not attach_status:
                print u"云盘挂载失败.."


def restart(server, server_cinder_info, nova1, cinder1):
    nova1.stop_server(server.id)
    nova1.start_server(server.id)


def Usage():
    print """
    Usage:
        start   : attach volume and start_vm
        stop    : detach volume and stop_vm,will save volume attach info in *.pkl file.
        attach  : according the *.pkl file to attach volume to the cloud server
        detach  : detach volume and save volume attach info in *.pkl file.
        restart : just stop and start cloud server .
    Config_file:
        config.py :config file is setting the tenant and other info ....
    """
    sys.exit("error")

# 操作函数
def operator(creds):
    # 获取操作函数
    if len(sys.argv) == 2:
        if sys.argv[1] == "start":
            func = start_vm
        elif sys.argv[1] == "stop":
            if os.path.exists('%s.pkl' % creds["project_id"]):
                c_time = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
                old_name = '%s.pkl%s' % (creds["project_id"], c_time)
                os.rename('%s.pkl' % creds["project_id"], old_name)
                if not os.path.exists("old_pkl"): os.mkdir("old_pkl")
                shutil.move(old_name, "old_pkl")
            func = stop_vm
        elif sys.argv[1] == "detach":
            # 卸载的时候要备份原来的pkl文件到old_pkl里面去。
            if os.path.exists('%s.pkl' % creds["project_id"]):
                c_time = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
                old_name = '%s.pkl%s' % (creds["project_id"], c_time)
                os.rename('%s.pkl' % creds["project_id"], old_name)
                if not os.path.exists("old_pkl"): os.mkdir("old_pkl")
                shutil.move(old_name, "old_pkl")
            func= detach_vm
        elif sys.argv[1] =="attach":
            func = attach_vm
        elif sys.argv[1] == "restart":
            func = restart
        else:
            Usage()
    else:
        Usage()
    cinder1 = Cinder("2", **creds)
    nova1 = Nova("2", cinder1, **creds)
    server_cinder_info = cinder1.get_attachments()
    # 如果存在相对应的pkl文件，那么就load值。
    if os.path.exists('%s.pkl' % creds["project_id"]):
        file1 = file('%s.pkl' % creds["project_id"], "rb")
        server_cinder_info = pickle.load(file1)
    else:
        # 如果不存在，那么就dump值
        file1 = file('%s.pkl' % creds["project_id"], "wb")
        pickle.dump(server_cinder_info, file1, True)
    all_server = nova1.get_server_list()
    for server in all_server:
        try:
            func(server, server_cinder_info, nova1, cinder1)
        except Exception, e:
            print e
            continue


            # restart_vm(server,server_cinder_info,nova1,cinder1)
            # args_list = [server,server_cinder_info,nova1,cinder1]
            # my_tp.append_job(func,args_list)
            # func(server,server_cinder_info,nova1,cinder1)
            # my_tp.wait_allcomplete()
            # while my_tp.result_queue.qsize():
            #    print my_tp.result_queue.get(),"restult"


# operator(creds)
start_time = time.clock()
for creds in config.user_creds_list:
    # print creds
    operator(creds, )
    # t = threading.Thread(target=operator,args=(creds,))
    # t.start()

end_time = time.clock()
# for i in range(100):
#     print threading.activeCount()
while threading.activeCount() - 1 != 0:
    end_time = time.clock()
print  "Process is run %f" % (end_time - start_time)

