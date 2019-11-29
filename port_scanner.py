#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author 郑彬彬
# @{DATE}
# github：https://github.com/zhengbinbin

import threading, queue, nmap
threads = []

class Scanner():
    def __init__(self, fileIn,fileOut):
        """端口扫描器"""
        self.nm = nmap.PortScanner()
        self.fileIn = fileIn
        self.fileOut = fileOut
        self.ipList = []
        self.host_list = []
        self.err = []
        self.ip_port = []
        self.length = 0
        self.last_ip = None
        self.last_port = None
        self.x = 0
        self.list = []


    def scan(self, ip):
        """探嗅端口的方法"""
        try:
            self.nm.scan(ip, '1-65535')
            for proto in self.nm[ip].all_protocols():
                lport = self.nm[ip][proto].keys()
                for port in lport:
                    r = self.nm[ip][proto][port]['state']
                    if r == 'open':
                        self.ip_port.append([ip, port])
                        #print(self.date_now + ip + ' ' + port)
                        print('%s %s' % (ip, port))
        except Exception as e:
            self.err.append(e)
            pass

    def check_open(self):
        """取出队列中排队的ip，将其送给scan方法"""
        while not self.q.empty():
            ip = self.q.get()
            self.scan(ip)

    def get_host(self):
        """将文本中host信息改为二维列表
        同时将ip写入ipList列表"""
        fi = open(self.fileIn, 'r+', encoding='UTF-8-sig')
        hosts = fi.readlines()
        for i in hosts:
            self.host_list.append(i.split())
        print(self.host_list)

        for host in hosts:
            ip = host.split()
            self.ipList.append(ip[0])
        print(self.ipList)
        fi.close()

    def put_queue(self):
        """将ipList中的ip单个取出放到队列q里面"""
        self.q = queue.Queue(maxsize=len(self.ipList))
        for ip in self.ipList:
            self.q.put(ip)

    def create_threads(self):
        """为check_open方法创建10线程，并将所有进程装进列表threads里面"""
        for i in range(5):
            t = threading.Thread(target=self.check_open)
            t.start()
            threads.append(t)

    def check_num(self):
        """判断列表里面的元素个数奇偶性，如奇就取最后一个保存起来"""
        self.length = len(self.ip_port)
        if (self.length % 2) == 1:
            self.last_ip = self.ip_port[-1][0]
            self.last_port = self.ip_port[-1][1]
            del self.ip_port[-1]
            self.length -= 1
        self.combine_port()

    def combine_port(self):
        """遍历列表，如果ip相同则将端口结合，同时将该二维数组设为['None', 'None']"""
        for i in self.ip_port:
            for j in range(self.x, self.length):
                if j < (self.length - 1):
                    if i[0] == self.ip_port[j + 1][0]:
                        if i[0] != 'None':
                            i[1] = str(i[1]) + ' ' + str(self.ip_port[j + 1][1])
                            self.ip_port[j + 1] = ['None', 'None']
            self.x = self.x + 1
        print(self.ip_port)

        for i in self.ip_port:
            # 将列表里非['None', 'None']元素全部添加到list_tmp_new列表中
            if i != ['None', 'None']:
                self.list.append(i)

        if self.last_ip != None:
            for i in self.list:
                if i[0] == self.last_ip:
                    i[1] = i[1] + ' ' + str(self.last_port)

        self.compare()

        with open(self.fileOut, 'a+', encoding='UTF-8-sig') as fo:
            for i in self.list:
                fo.write(str(i) + '\n')

    def compare(self):
        """比较list_tmp_new和host_list，取出负责人和系统信息"""
        for i in self.list:
            for j in self.host_list:
                if i[0] == j[0]:
                    i[1] = str(i[1]) + '  ' + str(j[1]) + '  ' + str(j[2])
                    break

if __name__ == '__main__':
    # fileIn = r'E:\fileIn.txt'
    # fileOut = r'E:\fileOut.txt'

    fileIn = r'/home/zhengbinbin/python/port_scanner/fileIn.txt'
    fileOut = r'/home/zhengbinbin/python/port_scanner/fileOut.txt'

    sc = Scanner(fileIn, fileOut)
    sc.get_host()
    sc.put_queue()
    sc.create_threads()
    #
    for t in threads:
        t.join()
    print('=============================')
    # 整理数据
    sc.check_num()