#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/7/23 16:07
# github:https://github.com/zhengbinbin
import subprocess, datetime, time, os, requests, socket

class proxy():
    def __init__(self,pppoeStart, pppoeStop, pppoeLog, time, checkUsefullog):
        """代理类"""
        self.pppoeStart = pppoeStart
        self.pppoeStop = pppoeStop
        self.pppoeLog = pppoeLog
        self.checkUsefullog = checkUsefullog
        self.time = time

        self.flag = 0
        self.flag3 = 0
    def pppoe(self):
        """拨号方法，每30mins拨号一次"""
        re = subprocess.call(self.pppoeStop, shell=True)
        if re == 0:
            time.sleep(1)
            subprocess.call(self.pppoeStart, shell=True)
        else:
            subprocess.call(self.pppoeStop, shell=True)
            time.sleep(1)
            subprocess.call(self.pppoeStart, shell=True)

    def checkIP(self):
        """检测IP是否通外网，再检测是否为最新IP"""
        response = requests.get('http://www.baidu.com')
        while self.flag < 5 and response.status_code != 200:
            self.flag += 1
            self.pppoe()

        with open(self.pppoeLog, 'a') as f:
            if  self.flag == 5 or self.flag3 == 5:
                f.write(self.time + '  ' + '连续 5 次拨号失败,机器将重启!!!!' + '\n')
                subprocess.call('/usr/bin/reboot', shell=True)

    def checkUseful(self):
        # 执行入库检测
        list = []
        flag2 = 0
        try:
            while True:
                result = int(os.popen('curl -s "http://114.215.206.140:8118/syncproxy?machine_id=$HOSTNAME&port=33381&source=zhengwen_yg_curl&purpose=指数微信正文采集"').read())
                re = int(result)
                if re == 0:
                    flag2 += 1
                    print('检查该ip为重复的IP，将再次进行拨号...')
                    self.pppoe()
                if re == 1:
                    # 拨号成功
                    print('拨号成功，这是一个新IP')
                    break
        except Exception as e:
            print('捕获到一个异常：' + e)
            self.flag3 += 1
            list.append(result)
            self.pppoe()

        with open(self.checkUsefullog, 'a') as f:
            re = os.popen('/sbin/ifconfig ppp0 |grep inet | awk "{print  $2}" |cut -d: -f2').read()
            A = re.split()  # A[1]是外网IP
            if flag2 != 0:
                f.write(self.time + '：连续 ' + str(flag2) + '次拨到重复的ip:' + '\n')
            if self.flag3 != 0:
                f.write('检查发现拨号异常：')
                for str in list:
                    f.write(str + ' ')
                f.write('\n')
            f.write('有效外网ip：' + A[1] + '\n')
            print('有效外网ip：' + A[1])

def main():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pppoeStart = '/usr/sbin/pppoe-start'
    pppoeStop = '/usr/sbin/pppoe-stop'
    pppoeLog = '/mnt/pppoeLog.log'
    checkUsefullog = '/mnt/checkUsefullog.log'


    p = proxy(pppoeStart, pppoeStop, pppoeLog, time, checkUsefullog)
    p.pppoe()
    p.checkIP()
    p.checkUseful()


if __name__ == '__main__':
    main()