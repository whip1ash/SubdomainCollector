#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
向https://dns.bufferover.run/dns 网站提取子域名,返回子域名集合
"""
from common.api import API
import requests,cfscrape

# 父类已经设置
# requests.adapters.DEFAULT_RETRIES = 5
# requests.packages.urllib3.disable_warnings()

class bufferover(API):

    def __init__(self,target):
        API.__init__(self)
        self.addr = "https://dns.bufferover.run/dns?q=%s"
        self.target = target
        self.module = "Bufferover接口查询"

    #绕过 Cloudflare 5s盾
    def query(self):

        url = self.addr % self.target
        try:
            scraper = cfscrape.create_scraper()
            data = scraper.get(url).content
            if not data:
                print "查询失败"
                return self.subdomains

            subdomain = self.match_domain(data)
            self.subdomains = self.subdomains.union(subdomain)
            return self.subdomains
        except Exception as e:
            print e
            return self.subdomains


if __name__ == '__main__':
    br = bufferover("wanmei.com")
    print br.query()


