#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
import requests
import time
from common.api import API

requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings()

class censys(API):

    def __init__(self,target):
        API.__init__(self)
        self.addr = 'https://www.censys.io/api/v1/search/certificates'
        self.target = target
        self.module = "Censys接口查询"
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
            resp = requests.post(url=self.addr,json=data,auth=(self.id,self.secret),proxies=self.proxies,verify=self.verify)
            # resp = requests.post(url=self.addr, json=data, auth=(self.id, self.secret), verify=self.verify)
            res = resp.json()
            if not resp.status_code == 200:
                print res
                print self.module + "模块花费时间为：" + str(self.end_time - self.start_time)
                return self.subdomains
            else:
                print self.module + "API有效"
            subdomains = self.match_domain(str(res))
            self.subdomains = self.subdomains.union(subdomains)
            pages = res.get("metadata").get("pages") + 1

            for page in range(2, pages):
                time.sleep(self.delay)
                data['page'] = page
                resp = requests.post(url=self.addr,json=data,auth=(self.id,self.secret),proxies=self.proxies,verify=self.verify)
                # resp = requests.post(url=self.addr, json=data, auth=(self.id, self.secret), verify=self.verify)
                if not resp.status_code == 200:
                    # print resp.json()
                    print "查询失败"
                    print self.module + "模块花费时间为：" + str(self.end_time - self.start_time)
                    return self.subdomains
                subdomains = self.match_domain(str(resp.json()))
                self.subdomains = self.subdomains.union(subdomains)
            # print self.subdomains

            self.end_time = time.time()
            print self.module +"模块花费时间为：" + str(self.end_time - self.start_time)
            return self.subdomains
        except Exception as e:
            print e
            print self.module + "模块花费时间为：" + str(self.end_time - self.start_time)
            return self.subdomains

if __name__ == '__main__':

    query = censys("baidu.com")
    print query.query()









