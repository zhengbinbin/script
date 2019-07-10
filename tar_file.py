#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/7/9 10:23
# github:https://github.com/zhengbinbin
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/7/4 17:20
# github:https://github.com/zhengbinbin

import tarfile, datetime, os


def compression(target, filename):
    """将文件压缩成tar格式"""
    cur_path = os.getcwd()
    target_path = os.path.dirname(filename)
    target_file = os.path.basename(filename)
    os.chdir(target_path)
    with tarfile.open(target, 'w:gz') as tar:
        tar.add(target_file)
    os.chdir(cur_path)
    os.remove(filename)

def Decompression():
    target = input('请输入需要解压的文件路径:')
    with tarfile.open(target) as tar:
        tar.extractall()
    os.remove(target)

def main():
    """tar文件的压缩和解压，python2.7不能使用with"""
    time = (datetime.datetime.now() - datetime.timedelta(minutes=3)).strftime('%Y-%m-%d(%H:%M:%S)')
    target = '/home/zhengbinbin/python/%s.pubsentiment-dev.access.log.tar.gz' % (time)
    filename = '/home/zhengbinbin/python/pubsentiment-dev.access.log'
    compression(target, filename)

    #Decompression()

if __name__ == '__main__':
    main()
    #/home/zhengbinbin/python/2019-07-09(11:15:45).pubsentiment-dev.access.log.tar.gz