#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author 郑彬彬
# @{DATE}
# github：https://github.com/zhengbinbin

import pexpect, os

PROMPT = ["# ", ">>> ", "> ", "\$ "]

def connect(port, user, ip, password):
    ssh_newkey = 'Are you sure you want to continue connecting (yes/no)?'
    connStr =  'ssh -p %s %s@%s' % (port, user, ip)
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[p|P]assword:'])
    if ret == 0:
        print('[-] Error Connecting!')
        return
    elif ret == 1:
        child.sendline('yes')
        if child.expect.TIMEOUT:
            print('[-] Error Connecting!')
            return
    child.sendline(password)
    child.expect(PROMPT)
    return child

def action(child, cmd,):
    child.sendline(cmd)
    child.expect(PROMPT)

def main():
    port = '52195'
    user = 'xtyunweiqbgw'
    ip = '10.117.185.250'
    password = 'E&OvP0suGQv4ID@m'
    cmd = 'touch a'
    child = connect(port, user, ip, password)
    action(child, cmd)

if __name__ == '__main__':
    main()

