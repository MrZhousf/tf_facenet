# -*- coding:utf-8 -*-
import logging
import time
import os
import config


def singleton(cls):

    instance = {}

    def _singleton(*args, **kw):
        if cls not in instance:
            instance[cls] = cls(*args, **kw)
        return instance[cls]

    return _singleton


class Log(object):
    """
    日志打印与日志文件保存
    """

    def __init__(self, name, log_dir):
        self.log_msg = '\n'
        self.log = logging.getLogger(name)
        self.log.setLevel(logging.INFO)
        log_txt = time.strftime("%Y-%m-%d", time.localtime())
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logfile = '%s%s.txt' % (log_dir, log_txt)
        # 输出到文件
        fh = logging.FileHandler(logfile, mode='a')
        fh.setLevel(logging.INFO)
        # 输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
        # formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.log.addHandler(fh)
        self.log.addHandler(ch)

    def info(self, msg):
        self.log.info(msg)

    def add(self, msg):
        """
        添加log信息
        最后调用do_log方法
        """
        msg += '\n'
        self.log_msg += msg

    def do_log(self):
        self.log_msg = self.log_msg.rstrip('\n')
        self.info(self.log_msg)
        self.log_msg = '\n'


@singleton
class LogAPI(Log):
    """
    API接口日志
    """
    LOG_DIR = config.CONFIG_LOG.api_log_dir

    def __init__(self, log_dir=''):
        Log.__init__(self, 'api', self.LOG_DIR)


@singleton
class LogErr(Log):
    """
    错误日志
    """
    LOG_DIR = config.CONFIG_LOG.error_log_dir

    def __init__(self):

        Log.__init__(self, 'error', self.LOG_DIR)


API = LogAPI()
ERROR = LogErr()

if __name__ == '__main__':
    a = LogAPI()
    a.add('1')
    a.add('2')
    a.do_log()
    b = LogErr()
    b.add('11')
    b.add('22')
    b.do_log()
    print a is b

