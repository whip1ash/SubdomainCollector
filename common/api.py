# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
API查询基类
"""

from utils import match
from utils import fake_header

import config
import time
import requests

requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings()


class API():

    def __init__(self):
        self.name = "API Query"         #模块名称
        self.module = ""                #子模块名称
        self.subdomains = set()         #存放的子域名
        self.ips = set()                #存放的IP

        self.debug = config.Debug       #调试开关
        self.target = ""                #目标域名
        self.proxies = config.proxies   #代理
        self.headers = fake_header.fake_header()     #http头
        self.addr = None                #Api接口地址
        self.verify = config.verify     #SSL 开关
        self.delay = 0                  #接口限制需要等待的时间

        self.start_time = time.time()   #模块开始的时间
        self.end_time  = None           #模块结束的时间
        self.costime = None             #花费的时间

    def match_domain(self,text):
        """
        利用正则匹配出resp中的子域名,若不存在，返回空集合
        :param text:
        :return: set()
        """
        return match.match(self.target,text)

    #中断睡眠
    def sleep(self):
        time.sleep(self.delay)
        return




