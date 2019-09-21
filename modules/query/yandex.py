#!/usr/bin/env python
# encoding: utf-8

'''
@author: whip1ash
@contact: security@whip1ash.cn
@software: pycharm 
@file: yandex.py
@time: 2019/9/20 16:55
@desc:
Yandex Api,including get the number of search results for the domain and get search content
Example:
    yandex = yandex(search_domain)
    count = yandex.search_count()

    yandex = yandex(search content)
    content = yandex.serch_content()
'''

from common.api import API
from common.utils.ApiException import ApiException
import config
import requests
import xml.etree.ElementTree as ET


class yandex(API):
    def __init__(self,query):
        API.__init__(self)
        self.addr = "https://yandex.com/search/xml?"
        self.query = query
        self.module = "Yandex查询接口"
        self.count = 0
        self.proxies = config.w_proxies

    def _query(self,url):
        res = ''
        self.url = self.addr + config.yandex_key + "&query=" + url
        if config.Debug:
            print self.url
        try:
            res = requests.get(url=self.url,proxies = self.proxies,headers=self.headers)
        except Exception as e:
           # Todo: log
            print e.message

        return res.text


    def _parse_xml(self,xml,mode='count'):
        """
        parse yandex return xml
        :param xml: xml returned by yandex
        :param mode: parser mode :  enumeration type : count , content
        :return:
            mode == count : int
            mode == content : {domain:[[url,title],[url,title]...]...}
            No result : False
        """
        tree = ET.fromstring(xml.encode('utf8'))
        response = tree.find('response')
        results = response.find('results')

        # 无搜索结果
        if results is None:
            error = response.find('error')
            if error.attrib['code'] == 15:
                # Sorry, there are no results for this search
                return False
            else:
                code = error.attrib['code']
                info = error.text
                raise ApiException('Yandex',code,info)

        grouping = results[0]

        # 只查找搜索结果数
        if mode == 'count':
            for ele in grouping.iter(tag='found'):
                if ele.attrib['priority'] == 'all':
                    return ele.text

        if mode == 'content':
            # content = {domain:[[url,title],[url,title]]}
            content = dict()
            # 默认只显示前二十条搜索结果，需要更多的搜索需要更改url，从yandex key中将参数拆出来
            for group in grouping.iter(tag='group'):
                url = group[2][1].text
                domain = group[2][2].text
                title = group [2][3].text

                if content.has_key(domain):
                    content[domain].append([url,title])
                else:
                    content[domain] = [[url,title]]

            if config.Debug:
                print content

            return content
        else:
            # 模式不存在
            return False

    def search_count(self):
        """
        Get the number of search results for a certain domain (self.query)
        :return: int
        """
        url = "site%3A" + self.query
        xml = self._query(url)

        try:
            self.count = self._parse_xml(xml)
        except ApiException as e:
            # Todo: log
            print e.message

        # 搜索结果为空
        if self.count == False:
            self.count = 0
            return  self.count

        if config.Debug:
            print "query = {} , count = {}".format(self.query,self.count)

        return self.count


    # 结果为空的时候是空字典
    def serch_content(self):
        """
        Get the top 20 search results.
        If search results are empty, then return a empty dict,and it will return a False if some .
        :return: {domain:[[url,title],[url,title]...]...}
        """
        xml = self._query(self.query)

        try:
            self.content = self._parse_xml(xml,'content')
        except ApiException as e:
            # Todo: log
            print e.message
            self.content = {}

        if self.content == False:
            return False

        return self.content

if __name__ == '__main__':
    # yandex = yandex("cs.wanmei.com")
    # count = yandex.search_count()
    # print count

    yandex = yandex("site%3Acdddaswertwerwers.wanmei.com")
    content = yandex.serch_content()