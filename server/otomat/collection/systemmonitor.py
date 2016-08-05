#_*_ coding: UTF-8 _*_
import sys,os
import psutil
import socket,fcntl,struct
reload(sys)
sys.setdefaultencoding('utf8')


class Monitor_systeminfo:
    def __init__(self):
        pass
    def Mem_info(self):
        mem = psutil.virtual_memory()
        return mem
    def Swap_info(self):
	swap = psutil.swap_memory()
        return swap
    def Cpu_Percent(self):
        cpu = psutil.cpu_percent()
	return cpu
    def disk_usage(self):
        disk = psutil.disk_usage("/")
        return disk
    def nic_io_ubuntu(self):
        nic = psutil.net_io_counters(pernic=False)
        return nic
    def nic_io_centos(self):
        nic = psutil.network_io_counters(pernic=False)
        return nic
    def hostname(self):
        host = socket.gethostname()
        return host
    def get_ip_address(self,ifname='eth0'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
                     s.fileno(),0x8915,  # SIOCGIFADDR
                    struct.pack('256s', ifname[:15])
         )[20:24])
    #def get_ip_address(self):
    #    s = socket.gethostbyname_ex(socket.gethostname())
    #    return s[2]
