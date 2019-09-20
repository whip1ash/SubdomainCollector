#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
向virustotal接口查询，返回子域名集合
"""

import requests
import config
from common.api import API

requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings()

class virustotal(API):

    def __init__(self,target):
        API.__init__(self)
        self.name = "Virustotal接口查询"
        self.addr = "https://www.virustotal.com//vtapi/v2/domain/report"
        self.api_key = config.virustotal_api_key
        self.target = target

    def query(self):
        params = {"apikey": self.api_key, "domain": self.target}
        try:
            # resp = requests.get(url=self.addr, headers=self.headers,params=params,proxies=self.proxies,verify=self.verify)
            resp = requests.get(url=self.addr, headers=self.headers,params=params,verify=self.verify)

            if resp.status_code is not 200:
                self.logger().error("API_KEY 错误")
                return self.subdomains
            else:
                self.logger().info("API调用成功")
            data = resp.json().get('subdomains')
            # print [i.encode("utf-8") for i in data]
            sub = set([i.encode("utf-8") for i in data])
            self.subdomains = self.subdomains.union(sub)

            return self.subdomains

        except Exception as e:
            self.logger().error("查询出错：" + str(e))
            return self.subdomains

    def run(self):
        """
        整合
        """
        self.query()
        self.save_data()

def do(target):
    """
    统一多线程调用
    :param target: 目标域名
    :return: NULL。直接存入队列
    """
    vt = virustotal(target)
    vt.run()


if __name__ == '__main__':
    vs = virustotal("wanmei.com")
    print vs.query()
    # do("wanmei.com")