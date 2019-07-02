#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author 郑彬彬
# @{DATE}
# github：https://github.com/zhengbinbin

import telnetlib, threading, queue

ipList = []

threads = []

class Scanner():
    def __init__(self, fileIn, fileOut):
        self.server = telnetlib.Telnet()
        self.fileIn = fileIn
        self.fileOut = fileOut

    def sniffing(self, ip, f):
        """探嗅端口的方法"""
        for port in range(20, 23):
            try:
                self.server.open(ip, port)
                f.write(str(ip) + ' ' + str(port) + '\n')

                print('{0} {1} is open.'.format(ip, port))
            except Exception as err:
                print('{0} {1} is not open.'.format(ip, port))
                #pass
            finally:
                self.server.close()

    def check_open(self, q):
        """检测队列中的信息"""
        f = open(self.fileOut, 'a')
        try:
            while True:
                ip = q.get_nowait()
                #print(ip)
                sc.sniffing(ip, f)
        except Exception as err:
            pass

        f.close()

    def get_host(self):
        f = open(self.fileIn, 'r+', encoding='UTF-8-sig')
        #f = open(self.fileIn, 'r+')
        hosts = f.readlines()
        for host in hosts:
            ip = host.split()
            ipList.append(ip[0])
        #print(ipList)
        f.close()
        return hosts

    def put_queue(self, q):
        for ip in ipList:
            q.put(ip)

    def create_threads(self, q):
        for i in range(500):
            t = threading.Thread(target=self.check_open, args=(q,))
            t.start()
            threads.append(t)

if __name__ == '__main__':
    fileIn = r'E:\test.txt'
    fileOut = r'E:\test1.txt'

    sc = Scanner(fileIn, fileOut)
    hosts = sc.get_host()
    #print(hosts)
    q = queue.Queue()
    sc.put_queue(q)
    sc.create_threads(q)

    for t in threads:
        t.join()

