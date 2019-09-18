#!/usr/bin/python
# -*- coding: utf-8 -*-
import dns.resolver
import config

def dns_resolver():
    """
    DNS解析器
    :return: 解析器对象
    """
    resolver = dns.resolver.Resolver()
    resolver.nameservers = config.resolver_servers
    resolver.timeout = config.resolver_timeout
    return resolver


def dns_resolver_A(domain):
    """
    解析A记录,返回解析出的ip集合
    :return:set()
    """
    resolver = dns_resolver()
    results = resolver.query(domain,"A")
    ttl = results.ttl
    ips = {item.address for item in results}
    return ips


if __name__ == '__main__':
    domain = "www.whip1ash.cn"
    answer = dns_resolver_A(domain)
    print answer

