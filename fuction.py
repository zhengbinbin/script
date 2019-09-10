#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/9/10 16:38
# github:https://github.com/zhengbinbin
import sys, argparse, urllib, json

def ipGetHostid(ip, url, auth):
    values = {'jsonrpc': '2.0',
              'method': 'host.get',
              'params': {

              }

    }
id = 'https://www.cnblogs.com/waynechou/p/zabbix_api.html'