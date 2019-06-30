#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @author 郑彬彬
# @{DATE}
# github：https://github.com/zhengbinbin

import telnetlib, threading, queue
THREADS = []

def get_ip_status(ip, fileOut):
    """取消队列，写一个类来完成"""
    server = telnetlib.Telnet()
    for port in range(0, 65535):
        try:
            server.open(ip, port)
            print('{0} port {1} is open'.format(ip, port))
            write_in(fileOut, port)

        except Exception as e:
            print('hhhh')
            pass
        finally:
            server.close()

def write_in(fileOut, port):
    f = open(fileOut, 'r+')
    print('111111')
    f.write(port)
    f.close()

def put_queue(q, fileIn):
    f = open(fileIn)
    values = f.readlines()
    for value in values:
        q.put(value)
    f.close()

def make_thread(q, fileOut):
    for i in range(100):
        t = threading.Thread(target=check_open, args=(q, fileOut)) #为每个ip的每个端口创建一个线程
        t.start()
        THREADS.append(t)

def check_open(q, fileOut):
    try:
        while True:
            value = q.get_nowait()
            A = value.split()
            ip = A[0]
            get_ip_status(ip, fileOut)
    except Exception as e:
        pass


if __name__ == '__main__':
    fileIn = r'E:\test.txt'
    fileOut = r'E:\test1.txt'
    q = queue.Queue() #创建一个队列
    put_queue(q, fileIn)
    make_thread(q, fileOut)


    for thread in THREADS: #该函数是主线程，join()的作用是当数组threads里面所有的进程执行结束后再执行主线程
        thread.join()