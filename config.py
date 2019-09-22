# -*- coding: utf-8 -*-
import random

#Debug
Debug = True

#DNS服务器
resolver_servers = [
    '114.114.114.114',
    '233.5.5.5',
    '233.6.6.6'
]
#DNS解析超时时间
resolver_timeout = 3.0

#SSL_Verify
verify = False

#本地测试代理
proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'https://127.0.0.1:8080'
}

# yandex走代理，否则ip不稳定
w_proxies = {
    'http' : 'socks5://127.0.0.1:1080',
    'https' : 'socks5://127.0.0.1:1080'
}

#UA头
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) '
    'Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/68.0']

#是否需要伪造IP
FAKE_IP = False

#Yandex token
#Yandex 限制了指定ip，故访问需要挂代理


yandex_key = "user=xxxxxxxxxxxx&key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&sortby=tm.order%3Dascending&filter=none&groupby=attr%3D%22%22.mode%3Dflat.groups-on-page%3D10.docs-in-group%3D1&lr=*"

# RiskIQ key
riskiq_key = {'xxxxxxxxxxx@xxxx.com':'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
       }
