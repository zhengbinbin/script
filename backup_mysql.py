#!/usr/bin/python
# @Author:郑彬彬
# @date: 2019/6/25 11:28
# github：https://github.com/zhengbinbin

import subprocess, os, tarfile, time

class mysql_bak():
    """定义一个备份mysql的类"""
    def __init__(self,date, user, password, database, backup_dir, logfile,
                          dumpfile, archive, remoteip, remotedir):
        self.date = date
        self.user = user
        self.password = password
        self.database = database
        self.backup_dir = backup_dir
        self.logfile = logfile
        self.dumpfile = dumpfile
        self.archive = archive
        self.remoteip = remoteip
        self.remotedir = remotedir

    def create_file(self, dirname, filename=None):
        self.dirname = dirname
        self.filename = filename
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        if not os.path.exists(self.logfile):
            os.mknod(self.logfile)

    def dump_mysql(self):
        """备份数据库"""

        # 检测文件和文件夹是否存在
        self.create_file(self.backup_dir, self.logfile)

        # 写入备份日期到日志文件
        f = open(self.logfile, 'a')
        f.write(self.date)

        os.chdir(self.backup_dir)
        dumpCmd = '/usr/local/mysql/bin/mysqldump -u' + self.user + ' -p' + self.password + ' ' + \
                  self.database + ' > ' + self.backup_dir + '/' + self.dumpfile
        result = subprocess.call(dumpCmd, shell=True)
        if result == 0:
            with tarfile.open((self.backup_dir + '/' +  self.archive), 'w:gz') as tar:
                tar.add(self.backup_dir + '/' + self.dumpfile, os.path.basename(self.backup_dir + '/' + self.dumpfile))
                f.write(' 备份成功')
                f.write('\n')
                os.remove((self.backup_dir + '/' + self.dumpfile))
        else:
            f.write(' 备份失败' + self.date)
            f.write('\n')
        f.close()

        self.rsync_mysql()

    def rsync_mysql(self):
        """使用该方法确保设置吗免密登录和目标主机建立了remotedir文件夹"""
        self.create_file(self.remotedir)
        cmd = 'rsync -av -e "ssh -p 52213" ' + self.backup_dir + '/' + ' xtyunweits@' + self.remoteip + ':' + self.remotedir
        print(cmd)
        subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    date = time.strftime('%Y-%m-%d', time.localtime())
    user = 'root'  # 设置mysql登陆用户名
    password = '7wg7QLyvNM8rVMT^'
    database = 'postfix'  # 要备份的数据库名
    backup_dir = '/home/zhengbb/bak/mysql'  # 备份数据库路径
    logfile = '/home/zhengbb/bak/log'  # 备份数据库日志文件
    dumpfile = date + '-mysql.sql'  # 备份后的文件名
    archive = dumpfile + '-tar.gz'  # 压缩后的文件名
    remoteip = '10.51.24.148'  # 异地备份机器ip（电信测试服务器）
    remotedir = '/home/xtyunweits/bak/mysql/'  # 异地备份目录

    # 创建mysql_bak类
    mysqlBack = mysql_bak(date, user, password, database, backup_dir, logfile,
                          dumpfile, archive, remoteip, remotedir)
    mysqlBack.dump_mysql()