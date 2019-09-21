#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
调用Censys接口,返回子域名集合
"""

import config
import requests
from common.api import API

# 父类已经设置
# requests.adapters.DEFAULT_RETRIES = 5
# requests.packages.urllib3.disable_warnings()

class censys(API):

    def __init__(self,target):
        API.__init__(self)
        self.addr = 'https://www.censys.io/api/v1/search/certificates'  #接口地址
        self.target = target
        self.name = "Censys接口查询"
        self.id = config.censys_api_id
        self.secret = config.censys_secret
        self.delay = 3    #免费接口查询限制，2.5s一次

    #向接口查询并匹配子域名
    def query(self):
        data = {
            "query": "parsed.names:" + self.target,
            "page": 1,
            "fields": ["parsed.subject_dn"],
            "flatten": True
        }
        # print data
        try:
            # resp = requests.post(url=self.addr,json=data,auth=(self.id,self.secret),headers=self.headers,proxies=self.proxies,verify=self.verify)
            resp = requests.post(url=self.addr, json=data, headers=self.headers,auth=(self.id, self.secret), verify=self.verify)
            res = resp.json()
            if not resp.status_code == 200:
                self.logger().error("API查询失败")
                return self.subdomains
            else:
                self.logger().info("API_Key有效")
            subdomains = self.match_domain(str(res))
            self.subdomains = self.subdomains.union(subdomains)
            pages = res.get("metadata").get("pages") + 1

            for page in range(2, pages):
                self.sleep()
                data['page'] = page
                # resp = requests.post(url=self.addr,json=data,auth=(self.id,self.secret),headers=self.headers,proxies=self.proxies,verify=self.verify)
                resp = requests.post(url=self.addr, json=data, auth=(self.id, self.secret), headers=self.headers,verify=self.verify)
                if not resp.status_code == 200:
                    # print resp.json()
                    self.logger().error("API查询失败")
                    return self.subdomains
                subdomains = self.match_domain(str(resp.json()))
                self.subdomains = self.subdomains.union(subdomains)
            # print self.subdomains

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
    cs = censys(target)
    cs.run()


if __name__ == '__main__':

    query = censys("wanmei.com")
    print query.query()









