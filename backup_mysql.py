#!/usr/bin/python
# @Author:郑彬彬
# @date: 2019/6/25 11:28
# github：https://github.com/zhengbinbin

import subprocess, os, tarfile, datetime, time

class mysql_bak():
    """定义一个备份mysql的类"""
    def __init__(self,date, user, password, database, backup_dir, logfile,
                          dumpfile, archive, remoteip, remotedir, re_date_nuix):
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
        self.re_date_nuix = re_date_nuix

    def create_file(self):
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        if not os.path.exists(self.logfile):
            os.mknod(self.logfile)

    def dump_mysql(self):
        """备份数据库"""

        # 检测文件和文件夹是否存在
        self.create_file()

        # 写入备份日期到日志文件
        f = open(self.logfile, 'a')
        f.write(self.date)

        os.chdir(self.backup_dir)
        dumpCmd = '/usr/local/mysql/bin/mysqldump -u' + self.user + ' -p' + self.password + ' ' + \
                  self.database + ' > ' + self.backup_dir + '/' + self.dumpfile
        #print(dumpCmd)
        result = subprocess.call(dumpCmd, shell=True)
        if result == 0:
            with tarfile.open((self.backup_dir + '/' +  self.archive), 'w:gz') as tar:
                tar.add(self.backup_dir + '/' + self.dumpfile)
                f.write(' 备份成功')
                f.write('\n')
                os.remove((self.backup_dir + '/' + self.dumpfile))
        else:
            f.write(' 备份失败' + self.date)
            f.write('\n')
        f.close()

        self.delete_bak()
        self.rsync_mysql()

    def rsync_mysql(self):
        """使用该方法确保设置免密登录和目标主机建立了remotedir文件夹"""
        cmd1 = 'rsync -av -e "ssh -p 52214" ' + self.backup_dir + '/' + ' xtyunweisolr406@' + self.remoteip + ':' + self.remotedir
        #cmd2 = 'rsync -av -e ssh ' + self.backup_dir + '/' + ' root@' + self.remoteip + ':' + self.remotedir
        print(cmd1)
        subprocess.call(cmd1, shell=True)

    def delete_bak(self):
        """只保留三天的数据"""
        for maindir, subdir, files in os.walk(self.backup_dir):
            for file in files:
                ret = os.path.getmtime(file)
                if ret < self.re_date_nuix:
                    os.remove(file)

if __name__ == '__main__':
    date = (datetime.datetime.now() - datetime.timedelta(minutes=3)).strftime('%Y-%m-%d-%H-%M-%S')
    user = 'root'  # 设置mysql登陆用户名
    password = '7wg7QLyvNM8rVMT^'
    database = 'postfix'  # 要备份的数据库名
    backup_dir = '/bak/mysql'  # 备份数据库路径
    logfile = '/bak/log'  # 备份数据库日志文件
    dumpfile = date + '-mysql.sql'  # 备份后的文件名
    archive = dumpfile + '.tar.gz'  # 压缩后的文件名
    remoteip = '10.46.67.243'  # 异地备份机器ip（电信测试服务器）
    remotedir = '/bak/mysql/'  # 异地备份目录
    date_delete = datetime.datetime.now() - datetime.timedelta(days=3)
    re_date_nuix = time.mktime(date_delete.timetuple())

    # 创建mysql_bak类
    mysqlBack = mysql_bak(date, user, password, database, backup_dir, logfile,
                          dumpfile, archive, remoteip, remotedir, re_date_nuix)
    mysqlBack.dump_mysql()