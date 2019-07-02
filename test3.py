#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/7/1 17:52
# github:https://github.com/zhengbinbin

def test(path):
    f = open(path)
    context = f.readlines()
    print(context)



if __name__ == '__main__':
    path = r'E:\test1.txt'
    test(path)