#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/7/23 16:07
# github:https://github.com/zhengbinbin
import subprocess, datetime, os, sys, time

def checkProxy(frequency):
    """每1分钟检查proxy进程是否在运行"""
    timeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    proxyProcessLog = '/mnt/checkProxy.log'
    flag = 0
    pid = os.popen('ps aux | grep proxy | grep -v "grep" | awk "{print $2}"').read()
    while len(pid) == 0 and flag < 3:
        flag += 1
        subprocess.call('nohup /usr/bin/python /home/qingbo/proxy.py ' + frequency + ' &', shell=True)
        time.sleep(1)
        pid = os.popen('ps aux | grep proxy | grep -v "grep" | awk "{print $2}"').read()

    if flag == 3:
        print('连续4次重启proxy进程失败，将重启机器,本次重启将写入日志/mnt/proxyProcessLog.log')
        with open(proxyProcessLog, 'a') as f:
            f.write(timeNow + ': 连续4次重启proxy进程失败，将重启机器\n')
        subprocess.call('/usr/sbin/reboot', shell=True)

def checkSquid():
    """每1分钟检查squid进程是否在运行"""
    squidLog = '/mnt/checkSquid.log'
    timeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    flag = 0
    string = os.popen('systemctl status squid | grep "running"').read()
    while len(string) == 0 and flag < 3:
        flag += 1
        subprocess.call('systemctl restart squid', shell=True)
        string = os.popen('systemctl status squid | grep "running"').read()

    if flag == 3:
        print('连续4次重启squid失败，将重启机器,本次重启将写入日志/mnt/squidLog.log')
        with open(squidLog, 'a') as f:
            f.write(timeNow + ': squid程序连续4次重启失败，将重启机器\n')
        subprocess.call('/usr/sbin/reboot', shell=True)

def main():
    if len(sys.argv) == 1:
        print('Usage: /usr/bin/python /home/qingbo/protectSqiudAndProxy.py time(minutes) ')
        sys.exit()

    frequency = sys.argv[1]
    checkProxy(frequency)
    checkSquid()

if __name__ == '__main__':
    main()

