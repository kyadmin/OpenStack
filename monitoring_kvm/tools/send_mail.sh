#!/bin/bash
send_mail(){
 LOGFILE1=mail_success
 LOGFILE2=mail_faild
 case $1 in 
 Successfully)
   ReceiveMail="wangyouyan@che001.com"
   echo "[`date +%Y-%m-%d` `date +%T`] You will  switching host,as a result to host switch successfully.
Greethings from ShiJiazhuang!!!" > ${LOGFILE1}
   /bin/mail -s "[Cloud] The $2 switch  - `date +%Y%m%d`" $ReceiveMail  < ${LOGFILE1}
   ;;
 Faild)
   ReceiveMail="wangyouyan@che001.com"
   echo "[`date +%Y-%m-%d` `date +%T`] You will  switching host,as a result to host switch Faild.Greethings from ShiJiazhuang!!!" > ${LOGFILE2}
   /bin/mail -s "[Cloud] The $2 switch  - `date +%Y%m%d`" $ReceiveMail  < ${LOGFILE2}
   ;;
esac
}

if [ $# = 2 ];then
  send_mail $1 $2
else
  echo "Usage:$0 action host"
  echo "Ex:   $0 Successfully|Faild openstak01"
fi
