#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/9/10 16:38
# github:https://github.com/zhengbinbin
import sys, argparse, urllib, json
from login import requestJson
dict = {}

def ipGetHostsid(ip, url, auth):
    values = {'jsonrpc': '2.0',
              'method': 'host.get',
              'params': {#'output': ["name"],
                         'filter': {
                             'ip': ip
                         },
                    },
              'auth': auth,
              'id': '0'
            }
    output = requestJson(url, values)
    #print(output)
    if len(output) == 0:
        print('没有该主机！')
    else:
        name = output[0]['name']
        hostid = output[0]['hostid']
        dict = {'name': name, 'hostid': hostid}
        return dict

def getHostsitemsid(hostid, itemsname, url, auth):
    values = {'jsonrpc': '2.0',
              'method': 'item.get',
              'params': {
                  'output': ['itemids'],
                  'hostids': hostid,
              'filter': {
                  'key_': itemsname,
                    },
              },
            'auth': auth,
            'id': '0'
    }
    output = requestJson(url, values)
    if len(output) == 0:
        return output
    else:
        return output[0]['itemid']

def getHostsitemsvalue(itemid, url, auth):
    values = {'jsonrpc': '2.0',
              'method': 'history.get',
              'params': {
                  #'output': 'extend',
                  'history': 0,
                  'itemids': itemid,
                  'sortfield': 'clock',
                  'sortorder': 'DESC',
                  #'limit': 10,
                  'start_time': 64800,
                  'stop_time': 64900
              },
              'auth': auth,
              'id': 0
    }
    output = requestJson(url, values)
    print(output)
    if len(output) == 0:
        return output
    else:
        return output[0]['value']





















