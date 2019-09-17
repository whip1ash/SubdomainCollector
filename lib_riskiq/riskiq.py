# -*- coding: UTF-8 -*-
# 突然发现riskiq挺好用的啊哈哈哈哈

import api_key
import requests
import json

class riskiq:
    def __init__(self,target,debug):
        self.debug = debug
        self.api_key = api_key.key
        self.api_username = []
        self.api_account_balance = dict()
        for key in self.api_key:
            self.api_username.append(key)
        self._check()
        self.subdomains = []
        self.target = target


    def _check(self):
        for username in self.api_username:
            key = self.api_key[username]

            if self.debug:
                print self.api_account_balance
            try:
                #res = requests.get("https://api.passivetotal.org/v2/account/quota",auth=(username,key),proxies={'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}).json()
                res = requests.get("https://api.passivetotal.org/v2/account/quota",auth=(username,key)).json()
                # print res
                if res.has_key('message'):
                    self.api_account_balance[username]=0
                else:
                    self.api_account_balance[username] = 15 - res['user']['counts']['search_api']

            except Exception ,e:
                raise e



    def _req(self,api, query):
        """ data = {'key1': 'value1', 'key2': 'value2'} """
        current_username = ''

        for username in self.api_account_balance:
            if self.api_account_balance[username]>0:
                current_username = username
                break
        if self.debug:
            print "Current username is "+current_username

        url = "https://api.passivetotal.org/v2" + api

        data = {'query':query}
        try:
            result = requests.post(url,
                                   data=data,
                                   auth=(current_username,self.api_key[current_username]),json=data)

            self.api_account_balance[current_username] = self.api_account_balance[current_username] - 1

            return result.json()
        except Exception, e:
            raise e
            # traceback.print_exc()
            # logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))
            # return empty requests object
            # return __requests__.models.Response()

    def get_subdomains(self):
        subdomain_data = []
        api='/enrichment/subdomains'
        res = self._req(api,self.target)

        if self.debug:
            print res

        if res.has_key('message') :
            #此处进入切换账号流程
            return False
        elif res['success'] is not True:
            return False

        for sub in res['subdomains']:
            subdomain_data.append("%s.%s"%(sub,self.target))

        self.subdomains = subdomain_data

#reverse proxy ip
    def get_passive_dns(self,rp_ip,):

        api = '/dns/passive'

        res = self._req(api,rp_ip)

        if res.has_key('message'):

            # 此处应该进入切换账号流程
            return False

        # 这里直接返回 不放在属性中 因为这里是遍历调用 每次结果都放在结果字典中

        return [return_data['resolve'] for return_data in res['results']]

#
# if __name__ == '__main__':
#     risk = riskiq()
#     print risk.get_subdomains('tanx.com')