# -*- coding: utf-8 -*-
import random

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

#模块API
#riskiq api_key
key = {'usergeng@gmail.com':'8ba92e8196427445ad69fd5eeb00eb14ebe7b13b9bfb5680910d335e6e5c0e5c',
       'pxrhtv95742@027168.com':'18706acf0310eac6113d5aca04647507fbd3edbca393b017b016ffdc248fafe6',
       'pinoxc45381@chacuo.net':'365840f8b2e50418a671ec92c84eefe8f46e07328d69eed0c717f1bbe8665fd3',
       'asrc_pentest@sina.com':'0c432bc032f7c506b2df39149535c8a2f1cd638c297190f61285b7d56f3559c0',
       'tniahy91785@chacuo.net':'13c82012014f479bc76b1a213b78864b06c61a518546112eb897cff97491eae2',
       'xrcapk39716@chacuo.net':'f6254afd431a8750bb2d4aeb68917d0c71b8c41d07f417d41bf530adda901ffe',
       'tjebql49307@chacuo.net':'a0ef91b9d6852e3f7d8ff986eeb9fd8736f6c0e3cdf317a6c5330339aef75e93',
       'wrqenb65283@chacuo.net':'0476d8b60abdb30bb74c1b62a8c5943188c7fc7156b8e12809bc4be174a86b4d',
       'zkchre74302@chacuo.net':'c91910761e51213ef9cb30d030073e821eec58197cbb279711d6de733f56d542'
       }

#censys api_key
censys_api_id = "307084fd-1958-4946-a9fd-4a1916909acd"
censys_secret = "369Xpz0JJSmzJEV3mTgHtbprjynMgEe9"

#
#chinaz api_key
chinaz_api = "5d1850d223a64fd0917d790cab010497"

#virustotal api_key
virustotal_api_key = "9b6319409c8a982cc9202b5899df9f5f511b05cb8f94e2a45548860c1d2b6dd8"

#securitytrails api_key free for 50 times
securitytrails_api_key  = "Q9kaomMt4069phyGVk4F2FBAp57abH4C"

#aizhan api
aizhan_api = "2157bf6df185b171b237e22fed66050d"

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
FAKE_IP = True
