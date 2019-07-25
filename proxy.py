#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/7/23 16:07
# github:https://github.com/zhengbinbin
import subprocess, datetime, time, os, requests, socket

class proxy():
    def __init__(self,pppoeStart, pppoeStop, pppoeLog, time):
        """创建多个线程执行类里面的方法"""
        self.pppoeStart = pppoeStart
        self.pppoeStop = pppoeStop
        self.pppoeLog = pppoeLog
        self.time = time

        self.flag = 0

    def pppoe(self):
        """拨号方法，每30mins拨号一次然后进程睡眠"""
        re = subprocess.call(self.pppoeStop, shell=True)
        if re == 0:
            time.sleep(1)
            subprocess.call(self.pppoeStart, shell=True)
        else:
            subprocess.call(self.pppoeStop, shell=True)
            time.sleep(1)
            subprocess.call(self.pppoeStart, shell=True)

        time.sleep(1800)

        #self.checkIP()

    def checkIP(self):
        """检测IP是否通外网，再检测是否为最新IP"""
        response = requests.get('http://www.baidu.com')
        while self.flag < 2 and response.status_code != 200:
            self.flag += 1
            self.pppoe()

        with open(self.pppoeLog, 'a') as f:
            if  self.flag == 2:
                f.write(self.time + '  ' + '连续两次拨号失败!!!!' + '\n')
                self.flag = 0

        # 执行入库检测
        while True:
            result = os.popen('curl -s "http://114.215.206.140:8118/syncproxy?machine_id=$HOSTNAME&port=33381&source=zhengwen_yg_curl&purpose=指数微信正文采集"').read()
            if result == 0:
                """"""






        #re = os.popen('/sbin/ifconfig ppp0 |grep inet | awk "{print  $2}" |cut -d: -f2').read()
        #A = re.split()  # A[1]是外网IP





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


    p = proxy(pppoeStart, pppoeStop, pppoeLog, time)


if __name__ == '__main__':
    main()