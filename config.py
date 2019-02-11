# -*- coding:utf-8 -*-
import os
import yaml
import base64


def singleton(cls):
    instance = {}

    def _singleton(*args, **kw):
        if cls not in instance:
            instance[cls] = cls(*args, **kw)
        return instance[cls]

    return _singleton


@singleton
class Server(object):
    """
    服务配置信息
    """

    def __init__(self):
        self.loaded = False
        self.host = None
        self.port = None
        self.use_ssl = False
        self.ssl_crt = None
        self.ssl_key = None
        self.debug = None
        self.secret_key = None
        self.per_process_gpu_memory_fraction = None
        self.face_model_file = None
        self.database_url = None

    def init(self,
             host,
             port,
             use_ssl,
             ssl_crt,
             ssl_key,
             debug,
             secret_key,
             per_process_gpu_memory_fraction,
             face_model_file,
             database_url):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.ssl_crt = ssl_crt
        self.ssl_key = ssl_key
        self.debug = debug
        self.secret_key = base64.b64encode(secret_key)
        self.per_process_gpu_memory_fraction = per_process_gpu_memory_fraction
        self.face_model_file = face_model_file
        self.database_url = database_url
        self.loaded = True
        return self

    def load(self, yml):
        if self.loaded:
            return self
        this_dir = os.path.dirname(os.path.abspath(__file__))
        server_config = yaml.load(open(os.path.join(this_dir, yml)))['server']
        return self.init(**server_config)

    def config_development(self):
        """
        开发环境
        """
        return self.load('config_development.yml')

    def config_production(self):
        """
        生产环境
        """
        return self.load('config_production.yml')


@singleton
class Log(object):

    def __init__(self):
        self.loaded = False
        self.api_log_dir = None
        self.error_log_dir = None

    def init(self, api_log_dir, error_log_dir):
        self.api_log_dir = api_log_dir
        self.error_log_dir = error_log_dir
        self.loaded = True
        return self

    def load(self, yml):
        if self.loaded:
            return self
        this_dir = os.path.dirname(os.path.abspath(__file__))
        server_config = yaml.load(open(os.path.join(this_dir, yml)))['log']
        return self.init(**server_config)

    def config_development(self):
        """
        开发环境
        """
        return self.load('config_development.yml')

    def config_production(self):
        """
        生产环境
        """
        return self.load('config_production.yml')


def development():
    return Server().config_development(), Log().config_development()


def production():
    return Server().config_production(), Log().config_production()


# 环境配置
CONFIG_SERVER, CONFIG_LOG = development()
