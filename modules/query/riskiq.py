#!/usr/bin/env python
# encoding: utf-8

'''
@author: whip1ash
@contact: security@whip1ash.cn
@software: pycharm 
@file: riskiq.py
@time: 2019/9/21 16:58
@desc:
RiskIq Api, including get subdomains and query domains by reverse proxy ip

rq = riskiq('wa2344444nmei.com')
subdomains = rq.get_subdomains()
if not subdomains:
    print error

rq = riskiq()
reverse_domains = rq.get_passive_dns('203.129.211.181')
if not reverse_domains:
    print error

rq = riskiq()
rq.reverse_ip = "2.2.2.2"
reverse_domains = rq.get_passive_dns()
if not reverse_domains:
    print error
'''

import config
import requests
from common.api import API
from common.utils.ApiException import ApiException

class riskiq(API):
    def __init__(self,target=''):
        API.__init__(self)
        self.api_key = config.riskiq_key
        self.api_username = []
        self.api_account_balance = dict()
        for key in self.api_key:
            self.api_username.append(key)

        try:
            self._check()
        except ApiException as e:
            #todo: log
            print e.message
            print "Initial RiskIq failed!"
            exit()

        self.subdomains = []
        self.target = target
        self.current_username = ''
        self.reverse_domain = list()
        self.reverse_ip = ''

    def _check(self):
        """
        Check the balance of RisqIq api account
        :return: internal interface, no return value
        """
        for username in self.api_username:
            key = self.api_key[username]

            if self.debug:
                print self.api_account_balance
            try:
                #res = requests.get("https://api.passivetotal.org/v2/account/quota",auth=(username,key),proxies={'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}).json()

                if self.debug:
                    res = requests.get(
                        "https://api.passivetotal.org/v2/account/quota",
                        auth=(username, key),
                        proxies=config.w_proxies
                                       ).json()
                else:
                    res = requests.get("https://api.passivetotal.org/v2/account/quota",auth=(username,key)).json()
                if res.has_key('message'):
                    self.api_account_balance[username]=0
                    raise ApiException("RiskIq",0,res['message'])
                else:
                    self.api_account_balance[username] = 15 - res['user']['counts']['search_api']

            except Exception as e:
                print e.message

    def _req(self,api, query):
        """
        Request to riskiq api
        :param api: remote api address
        :param query: query data
        :return: json
        If the results is empty, it will return a empty list.And it will return False if errors occured.
        """
        for username in self.api_account_balance:
            if self.api_account_balance[username]>0:
                self.current_username = username
                break

        if self.api_account_balance[self.current_username] == 0:
            raise ApiException('RiskIq',0,"Today's api quota is used up!")

        if self.debug:
            print "Current username is "+self.current_username

        url = "https://api.passivetotal.org/v2" + api

        data = {'query':query}
        try:
            result = requests.post(url,
                                   data=data,
                                   auth=(self.current_username,self.api_key[self.current_username]),json=data)

            self.api_account_balance[self.current_username] = self.api_account_balance[self.current_username] - 1

        except Exception, e:
            print e.message
            return False

        data = result.json()

        if data.has_key('message'):
            raise ApiException('RiskIq',0,data['message'])

        return data

    def get_subdomains(self):
        """
        Invoke get subdomains interface.
        :return: [subdomains,...]
        If the results is empty, it will return a empty list.And it will return False if errors occured.
        """
        api='/enrichment/subdomains'

        try:
            res = self._req(api,self.target)
            if res['success'] is not True:
                return False
            subdomains = res['subdomains']
        except ApiException as e:
            print e.message
            self.subdomains = []

        if subdomains:
            for sub in subdomains:
                self.subdomains.append("%s.%s"%(sub,self.target))

        return self.subdomains

#reverse proxy ip
    def get_passive_dns(self,reverse_ip=''):
        """
        Invode get passsive dns interface
        :param reverse_ip: str; this value will be used if self.reverse_ip is blank
        :return: list [reverse_domain,...]
        """
        api = '/dns/passive'

        try:
            if self.reverse_ip == '' and reverse_ip=='':
                return False
            elif reverse_ip != '':
                res = self._req(api,reverse_ip)
            else:
                res = self._req(api,self.reverse_ip)
            self.reverse_domain = [result['resolve'] for result in res['results']]
        except ApiException as e:
            # todo log
            print e.message
            self.reverse_domain = []

        return  self.reverse_domain


if __name__ == '__main__':
    # rq = riskiq('wa2344444nmei.com')
    # print rq.get_subdomains()

    rq = riskiq()
    print rq.get_passive_dns('203.129.211.181')