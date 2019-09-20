#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
向crtsh查询证书，返回子域名集合
"""

import requests
from common.api import API

requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings()

class crtsh(API):

    def __init__(self,target):
        API.__init__(self)
        self.name = "Crtsh证书查询"
        self.addr = "https://crt.sh/"
        self.target = target

    def query(self):
        params = {"output": "json", "q": self.target}
        try:
            resp = requests.get(url=self.addr, headers=self.headers,params=params,proxies=self.proxies,verify=self.verify)
            # resp = requests.get(url=self.addr, headers=self.headers,params=params,verify=self.verify)

            if resp.status_code is not 200:
                self.logger().error("查询错误")
                return self.subdomains
            else:
                self.logger().info("API调用成功")
            sub = self.match_domain(str(resp.json()))
            self.subdomains = self.subdomains.union(sub)

            return self.subdomains

        except Exception as e:
            self.logger().error("查询出错：" + str(e))
            return self.subdomains

if __name__ == '__main__':
    cs = crtsh("wanmei.com")
    print cs.query()