#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @author 郑彬彬
# @{DATE}
# github：https://github.com/zhengbinbin
import urllib, sys, json, argparse
from login import *
from fuction import *

#登录zabbix获取auth
auth = authenticate(url, username, passwd)
hostIP = '10.80.65.188'
name = ipGetHostsid(hostIP, url, auth)
hostid = name['hostid']
itemid = (getHostsitemsid(hostid, 'system.cpu.util[,idle]', url, auth))
print(itemid)
print(getHostsitemsvalue(itemid, url, auth))