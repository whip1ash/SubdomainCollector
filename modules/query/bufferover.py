#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
向https://dns.bufferover.run/dns 网站提取子域名,返回子域名集合
"""
from common.api import API
import requests,cfscrape

requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings()

class bufferover(API):

    def __init__(self,target):
        API.__init__(self)
        self.addr = "https://dns.bufferover.run/dns?q=%s"
        self.target = target
        self.name = "Bufferover接口查询"

    #绕过 Cloudflare 5s盾
    def query(self):

        url = self.addr % self.target
        try:
            scraper = cfscrape.create_scraper()
            data = scraper.get(url).content
            if not data:
                # print "查询失败"
                self.logger().error("API查询失败")
                # if self.debug:
                #     self.logger().debug(data)
                return self.subdomains
            else:
                self.logger().info("查询成功")
            subdomain = self.match_domain(data)
            self.subdomains = self.subdomains.union(subdomain)
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
    br = bufferover(target)
    br.run()


if __name__ == '__main__':

    br = bufferover("wanmei.com")
    print br.query()

    # do("wanmei.com")


