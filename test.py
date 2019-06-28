#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/6/28 16:42
# github:https://github.com/zhengbinbin

import pexpect
def login(ip, password, cmd):
    #action = ('ssh -p ' + port + ' ' + user + '@' + ip)
    child = pexpect.spawn('ssh root@%s "%s"' % (ip, cmd) )
    i = child.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
    if i == 0:
        child.sendline(password)
    elif i == 1:
        child.sendline('yes\n')
        child.expect('password:')
        child.sendline(password)
    child.sendline(cmd)

if __name__ == '__main__':
    ip = '10.117.185.250'
    password = 'E&OvP0suGQv4ID@m'
    cmd = 'touch a'
    login(ip, password,cmd)