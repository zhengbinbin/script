#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/7/23 16:07
# github:https://github.com/zhengbinbin
import subprocess, datetime, time, os, sys

class Proxy():
    def __init__(self, pppoeLog, checkUsefullog, port):
        """代理类，该脚本一直在后台执行，可设置睡眠时间，时间可设置或随机产生一个20-30分钟的数"""
        self.pppoeLog = pppoeLog
        self.checkUsefullog = checkUsefullog
        self.port = port

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
        flag = 0
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = os.popen('curl --connect-timeout 10 -s -w "%{http_code}" "www.baidu.com" -o /dev/null').read()
        while result != '200' and flag < 3:
            flag += 1
            self.pppoe()
            result = os.popen('curl --connect-timeout 10 -s -w "%{http_code}" "www.baidu.com" -o /dev/null').read()

        if  flag == 3:
            with open(self.pppoeLog, 'a') as f:
                f.write(date + '  ' + '连续 4 次拨号失败,将杀死proxy.py进程!!!!' + '\n')
                #print('连续 4 次拨号失败,将杀死proxy.py进程!!!!')
            subprocess.call("ps -aux | grep 'proxy.py' | grep -v 'grep' | awk '{print $2}' | xargs kill", shell=True)

    def checkUseful(self):
        """执行入库检测"""
        list = []
        flag1 = 0
        flag2 = 0
        flag3 = 0
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        while True:
            if self.port == '33381':
                result = os.popen('curl -s "http://114.215.206.140:8118/syncproxy?machine_id=$HOSTNAME&port=33381&source=zhengwen_yg_curl&purpose=指数微信正文采集"').read()
            else:
                result = os.popen('curl -s "http://114.215.206.140:8118/syncproxy?machine_id=$HOSTNAME&port=33382&source=public_curl&purpose=公共采集"').read()
            if result == '0':
                flag1 += 1
                print('检查该ip为重复的IP，将再次进行拨号...')
                self.pppoe()
                self.checkIP()
            elif result == '1':
                # 拨号成功
                print('拨号成功，这是一个新IP')
                flag2 += 1
                break
            else:
                print('请求API接口异常,将记录异常并重新请求')
                flag3 += 1
                list.append(result)
                if flag3 == 3:
                    # 连续4次请求异常将睡眠1分钟重新拨号
                    time.sleep(60)
                    self.pppoe()
                    self.checkIP()

        with open(self.checkUsefullog, 'a') as f:
            re = os.popen('/sbin/ifconfig ppp0 |grep inet | awk "{print  $2}" |cut -d: -f2').read()
            A = re.split()  # A[1]是外网IP
            if flag1 != 0:
                f.write(date + '：连续 ' + str(flag1) + '次拨到重复的ip:' + '\n')
            if flag2 == 1:
                f.write(date + ':有效外网ip：' + A[1] + '\n')
                print('有效外网ip：' + A[1])
            if flag3 != 0:
                f.write(date + '连续' + str(flag3) + '次请求API接口异常:')
                for string in list:
                    f.write(string + ' ')
                f.write('\n')

def main():

    port = sys.argv[1]
    sleepTime = int(sys.argv[2]) * 60

    pppoeLog = '/mnt/pppoe.log'
    checkUsefullog = '/mnt/checkUseful.log'

    p = Proxy(pppoeLog, checkUsefullog, port)

    p.getPppoe()

    while True:
        p.pppoe()
        p.checkIP()
        p.checkUseful()
        time.sleep(sleepTime)

if __name__ == '__main__':
    main()


