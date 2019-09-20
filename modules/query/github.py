#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
爬取github搜集子域名
"""
import requests,re
import config

from bs4 import BeautifulSoup
from common.api import API

requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings()

class github(API):

    def __init__(self,target):
        API.__init__(self)
        self.name = "Github 爬行"
        self.addr = "https://github.com/search"
        self.target = target
        self.email = config.github_email
        self.passwd = config.github_pass
        self.session = requests.Session()
        self.delay = 0.3  #睡0.3秒，缓一缓

    def login(self):
        """
        登录github种植session
        :return:成功返回True，失败返回False
        """

        login_url = "https://github.com/session"
        token = self.get_token()
        if not token:
            return False
        data = {
            "utf8" : "✓",
            "authenticity_token" : token,
            "login" : self.email,
            "password" : self.passwd
        }
        try:
            # resp = self.session.post(url=login_url, data=data, headers=self.headers,verify=self.verify)
            resp = self.session.post(url=login_url, data=data, headers=self.headers,verify=self.verify,proxies=self.proxies)
            if not resp.status_code == 200:
                self.logger().error("登录失败")
                return False
            login = re.search(r'"user-login" content="(.*?)"',resp.text)
            if not login:
                return False
            self.logger().info("登录成功!!!")
            return True
        except Exception as e:
            self.logger().error("登录失败," + str(e))
            return False


    def get_token(self):
        """
        获取登录时需要的token，成功返回token，失败返回NULL
        """

        token_url = "https://github.com/login"
        try:
            resp = self.session.get(url=token_url, headers=self.headers, proxies=self.proxies, verify=self.verify)
            # resp = self.session.get(url=token_url, headers=self.headers, verify=self.verify)
            if not resp.status_code == 200:
                self.logger().error("token获取失败")
            token = re.search(r'name="authenticity_token" value="(.*?)"', resp.text)
            if token:
               return token.group(1)
            return
        except Exception as e:
            self.logger().error("token获取失败" + str(e))
            return


    def query(self):
        """
        爬取并匹配子域名
        :return:
        """
        if not self.login():
            self.logger().error("登录失败!!!")
            return self.subdomains
        page = 0
        while True:
            page = page + 1
            data = {"q": self.target, "type": "Code", "p": page}
            self.sleep()
            try:
                resp = self.session.get(url=self.addr,params=data,headers=self.headers, proxies=self.proxies, verify=self.verify)
                # resp = self.session.get(url=self.addr,params=data,headers=self.headers, verify=self.verify)
                if not resp.status_code == 200:
                    if resp.status_code == 429:
                        #TODO:说明太多请求IP被封了,需要换代理
                        break
                    else:
                        break
                soup = BeautifulSoup(resp.content,"lxml")
                sub = self.match_domain(soup.text)
                if not sub:
                    break
                self.subdomains = self.subdomains.union(sub)
                if page > 100:
                    break
            except Exception as e:
                self.logger().error("获取失败" + str(e))
                break
        self.encode()
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
    gh = github(target)
    gh.run()


if __name__ == '__main__':

    gh = github("wanmei.com")
    print gh.query()
    # do("wanmei.com")
















