#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author 郑彬彬
# @{DATE}
# github：https://github.com/zhengbinbin

import telnetlib
import threading


def get_ip_status(ip, port):
    server = telnetlib.Telnet()
    try:
        server.open(ip, port)
        print('{0} port {1} is open'.format(ip, port))
    except Exception as err:
        pass
        #print('{0} port {1} is not open'.format(ip, port))
    finally:
        server.close()


if __name__ == '__main__':
    host = '112.124.120.67'
    threads = []
    for port in range(0, 65535):
        t = threading.Thread(target=get_ip_status, args=(host, port))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

#host = '112.124.120.67'
#host = '10.162.53.136'