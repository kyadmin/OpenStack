#!/bin/bash

check_port=`netstat -nltp|grep 18888|wc -l`

if [[ $check_port = 1 ]];then
   echo "server exist,noting to do...."
else
   python kvm_monitoring.py server &
fi
retry=`cat /root/script/monitoring_kvm/tools/mointoring_kvm.conf |grep retry |cut -d= -f2`
hello=`cat /root/script/monitoring_kvm/tools/mointoring_kvm.conf |grep hello |cut -d= -f2`
retry_time=`expr $retry \* $hello`

#server_stop=`ps -ef|grep -v grep|grep "python kvm_monitoring.py server"|awk '{print $2}'|xargs kill -9`

check_client_state=`cat /root/script/monitoring_kvm/tools/check_client_conn`

while :
do 
  echo "0" > /root/script/monitoring_kvm/tools/check_client_conn
  sleep $retry_time
  if [[ $check_client_state = 1 ]];then
	echo "noing to do..."
  elif [ $check_client_state = 0 ];then
	python kvm_monitoring.py work &
	echo "llllll"
  else
      echo "file state error...."
      echo "0" > /root/script/monitoring_kvm/tools/check_client_conn
  fi
done
