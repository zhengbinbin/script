#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author:郑彬彬
# @date: 2019/7/10 17:11
# github:https://github.com/zhengbinbin
import os, datetime, tarfile, sys

class check_files():
    """只保留最新的3个文件"""
    def __init__(self, path, bak_path, targetfile, log, date, file):
        self.path = path
        self.dict = {}
        self.file_ctime_list = []
        self.numbers = 3
        self.bak_path = bak_path
        self.targetfile = targetfile
        self.log = log
        self.date = date
        self.file = file

    def get_ctime(self):
        file_list = os.listdir(self.bak_path)
        for file in file_list:
            full_url = os.path.join(self.bak_path, file)
            if os.path.isfile(full_url):
                ctime = os.path.getctime(full_url)
                self.dict[full_url] = ctime
        self.file_ctime_list = sorted(self.dict.items(), key=lambda item:item[1])

    def remove_oldfile(self):
        length = len(self.file_ctime_list)
        if length <= self.numbers:
            pass
        else:
            for i in range(length - self.numbers ):
                os.remove(self.file_ctime_list[i][0])

    def back_jar(self):
        if not os.path.exists(self.bak_path):
            os.mkdir(self.bak_path)
        print(self.bak_path)
        print(self.log)
        if not os.path.isfile(self.log):
            os.mknod(self.log)

        os.chdir(self.bak_path)
        tar = tarfile.open(self.targetfile, 'w:gz')
        tar.add(self.file)
        tar.close()
        with open(self.log, 'a+') as f:
            f.write(self.date + ' 备份成功\n')

def main():
    path = '/data3/qbo-platform/modules/elastic-search-interface'
    bak_path = path + '/bak'
    time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    date = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    targetfile = bak_path + '/' + time + '.tar.gz'
    file = path + '/' + sys.argv[1]
    log = bak_path + '/log'
    checkFiles = check_files(path, bak_path, targetfile, log, date, file)
    checkFiles.back_jar()
    checkFiles.get_ctime()
    checkFiles.remove_oldfile()

if __name__ == '__main__':
    main()