#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests,random
import config
import json
import fake_header
import match_domain
requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings()

def ip2domain(ip,target):
    """
    调用爱站api去反查域名,得到子域名
    :param ip: 反查的ip
    :param ip: 目标域名如 wanmei.com
    :return: set()
    """
    proxies = config.proxies
    verify = config.verify
    headers = fake_header.fake_header()
    domains = set()

    api_key = config.aizhan_api
    url = "https://apistore.aizhan.com/site/dnsinfos/" + api_key
    params = {
        "query":ip,
        "page":1
    }
    resp = requests.get(url=url,params=params,proxies=proxies,headers=headers,verify=verify)
    info = resp.json()
    if not info.get("code") == 200000:
        #logger 报错
        #TODO:logger 报错
        return set()
    pages = info.get("data").get("total_pages")
    nums = info.get("data").get("total_num")
    domain = match_domain.match_domain(target,str(info))
    domains = domains.union(domain)
    for page in range(2,pages+1):
        params["page"] = page
        res = requests.get(url=url, params=params, proxies=proxies, headers=headers, verify=verify).json()
        if not res.get("code") == 200000:

            return domains
        ddomain = match_domain.match_domain(target,str(res))
        domains = domains.union(ddomain)
    return domains


if __name__ == '__main__':
    domain = "com"
    print ip2domain("180.96.32.96",domain)



