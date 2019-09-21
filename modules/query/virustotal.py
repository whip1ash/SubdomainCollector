#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
向virustotal接口查询，返回子域名集合
"""

import requests
import config
from common.api import API

# 父类已经设置
# requests.adapters.DEFAULT_RETRIES = 5
# requests.packages.urllib3.disable_warnings()

class virustotal(API):

    def __init__(self,target):
        API.__init__(self)
        self.addr = "https://www.virustotal.com//vtapi/v2/domain/report"
        self.api_key = config.virustotal_api_key
        self.target = target

    def query(self):
        params = {"apikey": self.api_key, "domain": self.target}
        try:
            # resp = requests.get(url=self.addr, headers=self.headers,params=params,proxies=self.proxies,verify=self.verify)
            resp = requests.get(url=self.addr, headers=self.headers,params=params,verify=self.verify)

            if resp.status_code is not 200:
                print "ApiKey is Error"
                return self.subdomains

            data = resp.json().get('subdomains')
            # print [i.encode("utf-8") for i in data]
            sub = set([i.encode("utf-8") for i in data])
            self.subdomains = self.subdomains.union(sub)
            return self.subdomains

        except Exception as e:
            print e
            return self.subdomains

if __name__ == '__main__':
    vs = virustotal("wanmei.com")
    print vs.query()