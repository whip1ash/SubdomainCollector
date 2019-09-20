#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
调用securitytrails API接口,存入数据库
"""

import requests
import config

from common.api import API
requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings()

class securitytrails(API):
    def __init__(self,target):
        API.__init__(self)
        self.name = "Securitytrails接口查询"
        self.target = target
        self.api_key = config.securitytrails_api_key
        self.addr = "https://api.securitytrails.com/v1/domain/"
        self.delay = 2  #免费用户

    def query(self):
        params = {"apikey": self.api_key}
        url = self.addr + self.target + "/subdomains"
        self.sleep()
        try:
            # resp = requests.get(url=url, params=params, headers=self.headers,proxies=self.proxies,verify=False)
            resp = requests.get(url=url, params=params, headers=self.headers, verify=False)

            if resp.status_code is not 200:
                # print "查询出错"
                self.logger().error("API查询失败")
                return self.subdomains
            else:
                self.logger().info("API_Key有效")
            data = resp.json()["subdomains"]
            sub = [i + "." + self.target for i in data]
            subb = set([i.encode("utf-8") for i in sub])
            if sub:
                self.subdomains = self.subdomains.union(subb)
                return self.subdomains
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
    st = securitytrails(target)
    st.run()


if __name__ == '__main__':

    sy = securitytrails("wanmei.com")
    print sy.query()

    # do("wanmei.com")