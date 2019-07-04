#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author 郑彬彬
# @{DATE}
# github：https://github.com/zhengbinbin

import telnetlib, threading, queue
threads = []

class Scanner():
    def __init__(self, fileIn, fileOut, fileResult):
        """端口扫描器"""
        self.server = telnetlib.Telnet()
        self.fileIn = fileIn
        self.fileOut = fileOut
        self.fileResult = fileResult
        self.ipList = []
        self.list_tmp = []
        self.list_tmp_new = []
        self.last = [[]]
        self.A = []
        self.host_list = []
        self.q = queue.Queue(maxsize=10000)
        self.x = 0
        self.length = 0
        self.fo = open(self.fileOut, 'r+')
        self.fi = open(self.fileIn, 'r+', encoding='UTF-8-sig')
        self.check_num_flag = False
        self.get_last_flag = False

    def sniffing(self, ip):
        """探嗅端口的方法"""
        for port in range(1, 65536):
            try:
                self.server.open(ip, port)
                self.fo.write(str(ip) + ' ' + str(port) + '\n')
                print('{0} {1} is open.'.format(ip, port))
            except Exception as err:
                print('{0} {1} is not open.'.format(ip, port))
                pass
            finally:
                self.server.close()
        self.fo.close()

    def check_open(self):
        """取出队列中排队的ip，将其送给sniffing方法"""
        try:
            while True:
                ip = self.q.get_nowait()
                #print(ip)
                sc.sniffing(ip)
        except Exception as err:
            pass

    def get_host(self):
        """将文本中host信息改为二维列表
        同时将ip写入ipList列表"""
        hosts = self.fi.readlines()
        for i in hosts:
            self.host_list.append(i.split())
        print(self.host_list)

        for host in hosts:
            ip = host.split()
            self.ipList.append(ip[0])
        print(self.ipList)
        self.fi.close()

    def put_queue(self):
        """将ipList中的ip单个去除放到队列q里面"""
        for ip in self.ipList:
            self.q.put(ip)

    def create_threads(self):
        """为check_open方法创建进程(最多500个)，并将所有进程装进列表threads里面"""
        for i in range(500):
            t = threading.Thread(target=self.check_open)
            t.start()
            threads.append(t)

    def seperate(self):
        """读取test1.txt内容，并将其保存在二维列表list_tmp里面"""
        fi = open(self.fileOut, 'r+', encoding='UTF-8-sig')
        ip_port = fi.readlines()
        for i in ip_port:
            self.list_tmp.append(i.split())
        self.length = len(self.list_tmp)
        fi.close()
        self.check_num_flag = self.check_num()
        self.combine_port()

    def check_num(self):
        """判断列表里面的元素个数奇偶性，如奇就取最后一个保存起来"""
        if (self.length % 2) == 1:
            self.A = self.list_tmp[-1]
            del self.list_tmp[-1]
            self.last[0] = self.A
            self.length -= 1
            return True

    def combine_port(self):
        """遍历列表，如果ip相同则将端口结合，同时将该二维数组设为['None', 'None']"""
        fr = open(self.fileResult, 'r+', encoding='UTF-8-sig')
        for i in self.list_tmp:
            for j in range(self.x, self.length):
                if j < (self.length - 1):
                    if i[0] == self.list_tmp[j + 1][0]:
                        if i[0] != 'None':
                            i[1] = i[1] + ' ' + self.list_tmp[j + 1][1]
                            self.list_tmp[j + 1] = ['None', 'None']
            self.x = self.x + 1

        for i in self.list_tmp:
            # 将列表里非['None', 'None']元素全部添加到list_tmp_new列表中
            if i != ['None', 'None']:
                self.list_tmp_new.append(i)

        if self.check_num_flag:
            # 如果list_tmp列表为奇数就调用get_last()方法
            self.get_last_flag = self.get_last()
            if not self.get_last_flag:
                self.list_tmp_new.append(self.A)

        self.compare()
        #print(self.list_tmp_new)

        for i in self.list_tmp_new:
            fr.write(str(i) + '\n')

        fr.close()

    def get_last(self):
        """如果列表list_tmp长度为奇数，则将最后一个元素与列表比较"""
        for i in self.list_tmp_new:
            if i[0] == self.last[0][0]:
                i[1] = i[1] + ' ' + self.last[0][1]
                return True

    def compare(self):
        """比较list_tmp_new和host_list，取出负责人和系统信息"""
        for i in self.list_tmp_new:
            for j in self.host_list:
                if i[0] == j[0]:
                    i[1] = i[1] + ' ' + j[1] + ' ' + j[2]
                    break
        #print(self.list_tmp_new)

if __name__ == '__main__':
    fileIn = r'E:\fileIn.txt'
    fileOut = r'E:\fileOut.txt'
    fileResult = r'E:\fileResult.txt'

    sc = Scanner(fileIn, fileOut, fileResult)
    sc.get_host()
    sc.put_queue()
    sc.create_threads()

    for t in threads:
        t.join()
    print('=============================')
    # 整理fileOut.txt里面的数据
    sc.seperate()