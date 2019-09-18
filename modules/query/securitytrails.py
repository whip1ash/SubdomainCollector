#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import config

from common.api import API
requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings()

"""
调用securitytrails API接口，返回子域名集合
"""

class securitytrails(API):
    def __init__(self,target):
        API.__init__(self)
        self.module = "Securitytrails接口查询"
        self.target = target
        self.api_key = config.securitytrails_api_key
        self.addr = "https://api.securitytrails.com/v1/domain/"
        self.delay = 2  #免费用户

    def query(self):
        params = {"apikey": self.api_key}
        url = self.addr + self.target + "/subdomains"
        self.sleep()
        try:
            resp = requests.get(url=url, params=params, proxies=self.proxies, verify=False)

            if resp.status_code is not 200:
                print "查询出错"
                return self.subdomains

            data = resp.json()["subdomains"]
            sub = [i + "." + self.target for i in data]
            subb = set([i.encode("utf-8") for i in sub])
            if sub:
                self.subdomains = self.subdomains.union(subb)
                return self.subdomains
            return self.subdomains

        except Exception as e:
            print e
            return self.subdomains

if __name__ == '__main__':

    sy = securitytrails("wanmei.com")
    print sy.query()
