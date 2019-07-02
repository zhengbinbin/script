#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/7/1 11:47
# github:https://github.com/zhengbinbin

import telnetlib
import threading
import queue


def seperate(path1, path2):
    f1 = open(path1, 'r+', encoding='UTF-8-sig')
    f2 = open(path2, 'r+', encoding='UTF-8-sig')
    ip_port = f1.readlines()
    #print(ip_port)
    list_tmp = []
    list_tmp1 = []
    for i in ip_port:
        list_tmp.append(i.split())

    list_tmp1 = list_tmp

    print(list_tmp)

    flag_i = 0
    flag_j = 0

    for i in list_tmp:
        # print(i)
        # print(i[0])
        # print(i[1])
        for j in list_tmp1:
            print(j[0])
        print('===========')
            # if i[flag_i][0] == j[flag_j][0]:
            #     i[1] = i[1] + ' ' + j[1]
            #     flag_i += 1
            #     flag_j += 1

    print(list_tmp)

    # for i in list_tmp:
    #     f2.write(i)

    f1.close()
    f2.close()


    #print(list_tmp)
    # dict_tmp = dict(list_tmp)
    # print(dict_tmp)


if __name__ == "__main__":
    path1 = r'E:\test1.txt'
    path2 = r'E:\test2.txt'
    seperate(path1, path2)