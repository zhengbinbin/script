#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/7/23 16:07
# github:https://github.com/zhengbinbin
import subprocess, datetime, time, os, sys

class proxy():
    def __init__(self, pppoeLog, checkUsefullog):
        """代理类，该脚本30分钟执行一次"""
        self.pppoeLog = pppoeLog
        self.checkUsefullog = checkUsefullog

        self.flag = 0
        self.flag3 = 0

    def getPppoe(self):
        """获得pppoe路径"""
        pppoe_path = os.popen('find /usr/* -name "pppoe"').read()
        A = pppoe_path.split()
        self.pppoeStart = A[0] + '-start'
        self.pppoeStop = A[0] + '-stop'

    def pppoe(self):
        """拨号方法"""
        subprocess.call(self.pppoeStop, shell=True)
        time.sleep(1)
        subprocess.call(self.pppoeStart, shell=True)

    def checkIP(self):
        """检测IP是否通外网"""
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = os.popen('curl --connect-timeout 10 -s -w "%{http_code}" "www.baidu.com" -o /dev/null').read()
        while result != '200' and self.flag < 3:
            self.flag += 1
            self.pppoe()
            result = os.popen('curl --connect-timeout 10 -s -w "%{http_code}" "www.baidu.com" -o /dev/null').read()

        if  self.flag == 3 or self.flag3 == 3:
            with open(self.pppoeLog, 'a') as f:
                f.write(date + '  ' + '连续 4 次拨号失败,机器将重启!!!!' + '\n')
                #print('连续 4 次拨号失败,机器将重启!!!!')
            subprocess.call('/usr/sbin/reboot', shell=True)

    def checkUseful(self):
        """执行入库检测"""
        list = []
        flag2 = 0
        flag1 = 0
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        while True:
            result = os.popen('curl -s "http://114.215.206.140:8118/syncproxy?machine_id=$HOSTNAME&port=33381&source=public_curl&purpose=公共采集"').read()
            if result == '0':
                flag2 += 1
                print('检查该ip为重复的IP，将再次进行拨号...')
                self.pppoe()
            elif result == '1':
                # 拨号成功
                print('拨号成功，这是一个新IP')
                flag1 += 1
                break
            else:
                print('出现一个异常,将记录异常并重新拨号')
                self.flag3 += 1
                list.append(result)
                self.pppoe()

        with open(self.checkUsefullog, 'a') as f:
            re = os.popen('/sbin/ifconfig ppp0 |grep inet | awk "{print  $2}" |cut -d: -f2').read()
            A = re.split()  # A[1]是外网IP
            if flag2 != 0:
                f.write(date + '：连续 ' + str(flag2) + '次拨到重复的ip:' + '\n')
            if self.flag3 != 0:
                f.write('检查发现拨号异常：')
                for string in list:
                    f.write(string + ' ')
                f.write('\n')
            if flag1 == 1:
                f.write(date + ':有效外网ip：' + A[1] + '\n')
                print('有效外网ip：' + A[1])

def main():

    if len(sys.argv) == 1:
        print('Usage: /usr/bin/python /home/qingbo/proxy.py time(minutes) ')
        sys.exit()

    sleepTime = int(sys.argv[1]) * 60

    pppoeLog = '/mnt/pppoe.log'
    checkUsefullog = '/mnt/checkUseful.log'

    p = proxy(pppoeLog, checkUsefullog)

    while True:
        p.getPppoe()
        p.pppoe()
        p.checkIP()
        p.checkUseful()
        time.sleep(sleepTime)

    # p.getPppoe()
    # p.pppoe()
    # p.checkIP()
    # p.checkUseful()
    # time.sleep(sleepTime)



if __name__ == '__main__':
    main()


