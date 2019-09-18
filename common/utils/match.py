# -*- coding: utf-8 -*-
import re
import requests

def match(domain,text):
    """
    利用正则匹配出resp中的子域名,若不存在，返回空集合
    :param domain: 目标域名
    :param text: resp内容
    :return: set()
    """
    regexp = r'(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.){0,}' \
             + domain.replace('.', r'\.')
    data = re.findall(regexp,text,re.I)
    if not data:
        return set()
    dealed = map(lambda s:s.lower(),data)
    return set(dealed)


if __name__ == '__main__':
    url = "http://www.wanmei.com/"
    resp = requests.get(url=url)

    print match("com",resp.content)

