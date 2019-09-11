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
hostIP = '10.46.67.243'
hostid = getHostid(hostIP, url, auth)
keys = (getKeys(hostid, url, auth))
itemslist = getItemids(hostid, keys, url, auth)
getValue(itemslist, url, auth)