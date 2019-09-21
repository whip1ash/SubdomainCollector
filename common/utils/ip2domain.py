#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import config
import fake_header
import match
requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings()

def ip2domain(ip,target):
    """
    调用爱站api去反查域名,返回子域名
    :param ip: 反查的ip
    :param target: 目标域名如 wanmei.com
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
    resp = requests.get(url=url,params=params,headers=headers,verify=verify)
    # resp = requests.get(url=url,params=params,proxies=proxies,headers=headers,verify=verify)
    info = resp.json()
    if not info.get("code") == 200000:
        #logger 报错
        #TODO:logger 报错
        return set()
    pages = info.get("data").get("total_pages")
    nums = info.get("data").get("total_num")
    domain = match.match_domain(target, str(info))
    domains = domains.union(domain)
    for page in range(2,pages+1):
        params["page"] = page
        # res = requests.get(url=url, params=params, proxies=proxies, headers=headers, verify=verify).json()
        res = requests.get(url=url, params=params, headers=headers, verify=verify).json()
        if not res.get("code") == 200000:

            return domains
        ddomain = match.match_domain(target, str(res))
        domains = domains.union(ddomain)
    return domains


if __name__ == '__main__':
    domain = "com"
    print ip2domain("180.96.32.96",domain)



