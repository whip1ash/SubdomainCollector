#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
伪造header头部
"""

import random
import config

def fake_ip():
    """
    生成随机ip
    :return: ip
    """
    rip = lambda: '.'.join([str(int(''.join([str(random.randint(0, 2)), str(random.randint(0, 5)), str(random.randint(0, 5))]))) for _ in range(4)])
    return rip()




def fake_header():
    """
    伪造http请求头
    :return: dict{http头}
    """
    ua = random.choice(config.user_agents)
    headers = {}
    headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
    headers["Accept-Encoding"] = "gzip, deflate"
    headers["User-Agent"] = ua
    headers["Accept-Language"] = "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
    headers["Cache-Control"] = "max-age=0"
    if config.FAKE_IP:
        ip = fake_ip()
        headers["X-Forwarded-For"] = ip
        headers["X-Real-IP"] = ip
    return headers


if __name__ == '__main__':
    print fake_header()