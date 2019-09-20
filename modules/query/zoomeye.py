#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
调用zoomeye去查子域名，返回子域名集合
"""

import requests
import config
from common.api import API


requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings()

class zoomeye(API):

    def __init__(self,target):
        API.__init__(self)
        self.name = "Zoomeye 查询"
        self.addr = "https://api.zoomeye.org/web/search"
        self.user = config.zoomeye_username
        self.passwd = config.zoomeye_pass
        self.target = target

    def login(self):
        """
        登录系统获取 access_token
        :return: access_token
        """
        url = "https://api.zoomeye.org/user/login"
        data = {"username":self.user,"password":self.passwd}
        try:
            resp = requests.post(url=url,json=data,headers=self.headers,proxies=self.proxies,verify=self.verify)
            if not resp.status_code == 200:
                self.logger().error("账号密码错误")
            else:
                self.logger().info("登录成功")

            token = resp.json().get("access_token")
            return token
        except Exception as e:
            self.logger().error("登录出错：" + str(e))
            return

    def query(self):
        access_token = self.login()
        page = 1
        if not access_token :
            self.logger().error("登录失败")
            return self.subdomains
        self.headers["Authorization"] = "JWT "+access_token
        data = {"query":"hostname:"+self.target,"page":page}
        try:
            while True:
                # resp = requests.get(url=self.addr, headers=self.headers,params=data,proxies=self.proxies,verify=self.verify)
                resp = requests.get(url=self.addr, headers=self.headers,params=data,verify=self.verify)
                if resp.status_code is not 200:
                    self.logger().error("查询错误")
                    break
                self.logger().info("API调用成功")
                sub = self.match_domain(str(resp.json()))
                self.subdomains = self.subdomains.union(sub)
                page  = page + 1
                data["page"] = page

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
    ze = zoomeye(target)
    ze.run()

if __name__ == '__main__':
    ze = zoomeye("wanmei.com")
    print ze.query()
    # do("wanmei.com")