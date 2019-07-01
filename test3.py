#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/7/1 17:52
# github:https://github.com/zhengbinbin

def get_host(fileIn):
    f = open(fileIn, 'r+', encoding='UTF-8')
    hosts = f.readlines()
    ipList = []
    for host in hosts:
        #print(host)
        ip = host.split()
        ipList.append(ip[0])

    print(ipList)

if __name__ == '__main__':
    fileIn = r'E:\test.txt'
    get_host(fileIn)