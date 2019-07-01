#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @author 郑彬彬
# @{DATE}
# github：https://github.com/zhengbinbin

import telnetlib, threading, queue
THREADS = []

def test(fileIn, fileOut):
    fi = open(fileIn, 'r')
    fo = open(fileOut, 'r+')

    lines_seen = set()

    # for line in fi:
    #     line = line.strip('\n')
    #     print(line)
    #     if line not in lines_seen:
    #         fo.write(line + '\n')
    #         lines_seen.add(line)

    ts = fi.readlines()
    print(ts)

    fi.close()
    fo.close()



fileIn = r'E:\test1.txt'
fileOut = r'E:\test4.txt'
test(fileIn, fileOut)