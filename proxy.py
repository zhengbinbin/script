#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/7/23 16:07
# github:https://github.com/zhengbinbin
import subprocess, datetime, time, os, requests

class proxy():
    def __init__(self,pppoeStart, pppoeStop, pppoeLog):
        """创建多个线程执行类里面的方法"""
        self.pppoeStart = pppoeStart
        self.pppoeStop = pppoeStop
        self.pppoeLog = pppoeLog
        self.flag = 0

    def pppoe(self):
        """拨号方法，每30mins拨号一次，拨号之后调用check()方法，直到拨号成功，进程睡眠"""
        re = subprocess.call(self.pppoeStop, shell=True)
        if re == 0:
            time.sleep(1)
            subprocess.call(self.pppoeStart, shell=True)
        else:
            subprocess.call(self.pppoeStop, shell=True)
            time.sleep(1)
            subprocess.call(self.pppoeStart, shell=True)
        time.sleep(1800)

        self.checkIP()

    def checkIP(self):
        """检测IP是否通外网，再检测是否为最新IP"""
        response = requests.get('http://www.baidu.com')
        if self.flag < 2 and response.status_code != 200:
            self.flag += 1
            self.pppoe()

        subprocess.call('curl --connect-timeout 10 -s -w "%{http_code}" "www.baidu.com" -o /dev/null', shell=True)
        re = os.popen('/sbin/ifconfig ppp0 |grep inet | awk "{print  $2}" |cut -d: -f2').read()
        A = re.split()





    def sendInfo(self):
        """动态IP入库"""

    def checkBasic(self):
        """检查网络和squid程序"""





def main():
    #output = subprocess.Popen('find /usr/*  -name pppoe', shell=True, stdout=subprocess.PIPE)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pppoeStart = '/usr/sbin/pppoe-start'
    pppoeStop = '/usr/sbin/pppoe-stop'
    pppoeLog = '/mnt/pppoeLog.log'


    p = proxy(pppoeStart, pppoeStop, pppoeLog)


if __name__ == '__main__':
    main()