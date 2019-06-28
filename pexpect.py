#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/6/28 15:59
# github:https://github.com/zhengbinbin

# -*- coding: utf-8 -*-
# @Author  : Lan126

import pexpect

PROMPT = ["# ", ">>> ", "> ", "\$ "]


def connect(user, host, password):
    ssh_newkey = "Are you sure you want to continue connecting"
    connStr = "ssh " + user + "@" + host
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, "[p|P]assword:"])
    if ret == 0:
        print("[-] Error Connecting")
        return
    if ret == 1:
        child.sendline("yes")
        ret = child.expect([pexpect.TIMEOUT, "[p|P]assword:"])
        if ret == 0:
            print("[-] Error Connecting")
            return
    child.sendline(password)
    child.expect(PROMPT)
    return child


def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print((child.before).encode("utf-8"))


def main():
    host = "10.111.199.20"
    user = "root"
    password = "7TdyvNLijG!59%4j"
    child = connect(user, host, password)
    send_command(child, "cat /etc/shadow | grep root")

if __name__ == "__main__":
    main()