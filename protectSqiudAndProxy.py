#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/7/23 16:07
# github:https://github.com/zhengbinbin
import subprocess, datetime, os, sys, time, random

class ProtectSqiudAndProxy():
    """检查proxy、squid和sendCheck进程的类"""
    def __init__(self,port, frequency, proxyProcessLog, squidLog, sendCheckLog, timeNow):
        self.port = port
        self.frequency = frequency
        self.proxyProcessLog = proxyProcessLog
        self.squidLog = squidLog
        self.sendCheckLog = sendCheckLog
        self.timeNow = timeNow

    def checkProxy(self,):
        """每1分钟检查proxy进程是否在运行"""
        flag = 0
        pid = os.popen("ps aux | grep 'proxy.py' | grep -v 'grep' | awk '{print $2}'").read()
        while len(pid) == 0 and flag < 3:
            flag += 1
            subprocess.call('nohup /usr/bin/python /home/qingbo/proxy.py ' + self.port + ' ' + self.frequency + ' > /dev/null 2>&1 &', shell=True)
            time.sleep(3)
            pid = os.popen("ps aux | grep 'proxy.py' | grep -v 'grep' | awk '{print $2}'").read()

        if flag == 3:
            print('连续4次重启proxy进程失败，将结果写入日志/mnt/proxyProcessLog.log')
            with open(self.proxyProcessLog, 'a') as f:
                f.write(self.timeNow + ': 连续3次重启proxy.py进程失败,将杀死所有proxy.py进程\n')
            subprocess.call("ps -aux | grep 'proxy.py' | grep -v 'grep' | awk '{print $2}' | xargs kill", shell=True)


    def checkSquid(self,):
        """每1分钟检查squid进程是否在运行"""
        string = os.popen('systemctl status squid | grep "running"').read()
        if len(string) == 0:
            re = subprocess.call('systemctl restart squid', shell=True)
            if re != 0:
                with open(self.squidLog, 'a') as f:
                    f.write(self.timeNow + ': squid程序重启失败...\n')

    def sendCheck(self,):
        """检查sendCheck脚本是否在后台运行"""
        flag = 0
        pid = os.popen("ps aux | grep 'sendCheck.py' | grep -v 'grep' | awk '{print $2}'").read()
        while len(pid) == 0 and flag < 3:
            flag += 1
            subprocess.call('nohup /usr/bin/python /home/qingbo/sendCheck.py' + ' ' + self.port + ' & > /dev/null 2>&1 &', shell=True)
            time.sleep(3)
            pid = os.popen("ps aux | grep 'sendCheck.py' | grep -v 'grep' | awk '{print $2}'").read()

        if flag == 3:
            with open(self.sendCheckLog, 'a') as f:
                f.write(self.timeNow + ':连续3次重启sendCheck.py进程失败,将杀死所有sendCheck.py进程\n')
            subprocess.call("ps -aux | grep 'sendCheck.py' | grep -v 'grep' | awk '{print $2}' | xargs kill", shell=True)

def main():
    port = sys.argv[1]
    if len(sys.argv) == 2:
        # 如果没有传参数，则随机生成一个20-30之间的数
        frequency = str(random.randint(20, 30))
    else:
        # 如果穿了参数就将参数给到frequency
        frequency = sys.argv[2]

    proxyProcessLog = '/mnt/checkProxy.log'
    squidLog = '/mnt/checkSquid.log'
    sendCheckLog = '/mnt/sendCheck.log'
    timeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pt = ProtectSqiudAndProxy(port, frequency, proxyProcessLog, squidLog, sendCheckLog, timeNow)
    # while True:
    #     pt.checkProxy()
    #     pt.checkSquid()
    #     pt.sendCheck()
    #     time.sleep(60)

    pt.checkProxy()
    pt.checkSquid()
    pt.sendCheck()
    time.sleep(60)



if __name__ == '__main__':
    main()