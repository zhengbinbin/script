#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/7/11 16:12
# github:https://github.com/zhengbinbin

import queue

class Compare_txt():
    """比较两个txt文件的差异"""
    def __init__(self, fileIn, fileOut, fileResult):
        self.fileIn = fileIn
        self.fileOut = fileOut
        self.fileResult = fileResult
        self.result = []

    def compare(self):
        """分别读取两个文件的ip列表"""
        with open(self.fileIn, 'r') as f1:
            ip_new = f1.readlines()

        with open(self.fileOut, 'r') as f2:
            ip_old = f2.readlines()

        for ip_o in ip_old:
            for ip_n in ip_new:
                if ip_o != ip_n:
                    self.result.append(ip_o)

        with open(self.fileResult, 'a+') as fr:
            for ip in self.result:
                fr.write(ip)

if __name__ == '__main__':
    fileIn = r'E:/ip_new.txt'
    fileOut = r'E:/ip_old.txt'
    fileResult = r'E:/result.txt'
    re = Compare_txt(fileIn, fileOut, fileResult)
    re.compare()