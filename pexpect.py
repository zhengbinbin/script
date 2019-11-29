#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author 郑彬彬
# @{DATE}
# github：https://github.com/zhengbinbin
#pythpn2上面在不不同服务器上更新代码

import pexpect, commands, sys

PROMPT = ["# ", ">>> ", "> ", "\$ "]

def connect(user, ip, password):
    ssh_newkey = 'Are you sure you want to continue connecting (yes/no)?'
    connStr =  'ssh %s@%s' % (user, ip)
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[p|P]assword:'], timeout=200)
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

def update(updateDir):
    """update from svn"""
    commands.getoutput('svn up ' + updateDir)
    commands.getoutput('chmod -R 744 ' + updateDir)
    commands.getoutput('chown -R nginx.nginx ' + updateDir)

def action_remote(child, updateDir):
    child.sendline('svn up ' + updateDir)
    child.sendline('chmod -R 744 ' + updateDir)
    child.sendline('chown -R nginx.nginx ' + updateDir)
    child.expect(PROMPT)

def main():
    if len(sys.argv) == 1:
        print('usage: ./update updateDir')
        sys.exit()
    updateDir = sys.argv[1]
    user = 'root'
    ip_remote = ['172.17.94.3', '172.17.94.4']
    password = 'Yjs2019@CLOUD!'
    for ip in ip_remote:
        child = connect(user, ip, password)
        action_remote(child, updateDir)
        print(ip + ': update success')

    update(updateDir)
    print('172.17.94.2 update success!')

if __name__ == '__main__':
    main()

