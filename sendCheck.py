#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/8/1 9:46
# github:https://github.com/zhengbinbin
import time, sys, os

def noIndatabase(port):
    """本方法将机器送往松哥的python检查，不进入数据库"""
    while True:
        if port == '33381':
            re= os.popen('curl -s "http://114.215.206.140:8118/syncproxy?machine_id=$HOST_NUMBER&port=33381&source=zhengwen_yg_curl&purpose=指数微信正文采集&check=1"').read()
        else:
            re = os.popen('curl -s "http://114.215.206.140:8118/syncproxy?machine_id=$HOST_NUMBER&port=33382&source=public_curl&purpose=公共采集&check=1"').read()
        time.sleep(30)
def main():
    port = sys.argv[1]
    noIndatabase(port)

if __name__ == '__main__':
    main()