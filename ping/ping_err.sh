#!/bin/bash


echo "" > ip_unreachable
while read line
do
  #ping -c 3 $line  |grep '3 packets transmitted'|grep -v "0% packet loss" -a -B 3 |tee ip_unreachable
  ping -c 3 $line  |grep '3 packets transmitted, 0 received, +3 errors, 100% packet loss,' -B 1 >> ip_lllll

done < ip_List
