#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/9/10 16:38
# github:https://github.com/zhengbinbin
import sys, argparse, urllib, json
from login import requestJson
dict = {}
dict_keys = {}
dict_items = []

def getHostid(ip, url, auth):
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
    if len(output) == 0:
        print('没有该主机！')
    else:
        name = output[0]['name']
        hostid = output[0]['hostid']
        global dict
        dict = {'name': name, 'ip': ip}
        return hostid

def getKeys(hostid, url, auth):
    values = {'jsonrpc': '2.0',
              'method': 'item.get',
              'params': {
                  'output': ['itemids', 'key_'],
                  'hostids': hostid,
              },
            'auth': auth,
            'id': '0'
    }
    output = requestJson(url, values)
    print(output)
    if len(output) == 0:
        return output
    else:
        global dict_keys
        dict_keys = {'cpu_idle': 'vm.memory.size[available]', 'memory_available': 'system.cpu.util[,idle]',
                      'memory_total': 'vm.memory.size[total]'}

        return dict_keys

def getItemids(hostid, keys, url, auth):
    for key in keys.values():
        print(key)
        values = {'jsonrpc': '2.0',
                  'method': 'item.get',
                  'params': {
                      'output': ['itemids'],
                      'hostids': hostid,
                  'filter': {
                      'key_': key,
                        },
                  },
                'auth': auth,
                'id': '0'
        }
        output = requestJson(url, values)
        if len(output) == 0:
            return output
        else:
            global dict_items
            dict_items.append(output[0]['itemid'])

    return dict_items

def getValue(itemslist, url, auth):
    for itemid in itemslist:
        int(itemid)
        print(itemid)
        values = {'jsonrpc': '2.0',
                  'method': 'history.get',
                  'params': {
                      'output': 'extend',
                      'history': 0,
                      'itemids': itemid,
                      'sortfield': 'clock',
                      'sortorder': 'DESC',
                      'limit': 1,
                      # 'start_time': 1567628400,
                      # 'stop_time': 1568166904
                  },
                  'auth': auth,
                  'id': 0
        }
        output = requestJson(url, values)
        print(output)
        # cpu_idle_time = 0
        # if len(output) == 0:
        #     return output
        # else:
        #     for i in range(len(output)):
        #         cpu_idle_time = cpu_idle_time + float(output[i]['value'])
        #     average_cpu_idle_time = round(cpu_idle_time / len(output), 2)
        #     global dict
        #     dict['cpu_idle_time'] = average_cpu_idle_time
        #     print(dict)

















