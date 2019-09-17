# -*- coding: UTF-8 -*-
# 人生已看淡，不服就是干！服吗？不服！干他娘的！

import sys;
sys.path.append('lijiejie');
from lijiejie.SubNameBrute import SubNameBrute;
from lijiejie.SubNameBrute import lijiejie_options;
sys.path.append('lib_riskiq')
from lib_riskiq.riskiq import riskiq

import dns.resolver
import requests
import xml.etree.ElementTree as ET
import re


def lijiejie(target):
    # 现在这里的options在debug的模式中，正式使用的时候需要更改
    api_options = lijiejie_options()
    d = SubNameBrute(target=target, options=api_options)
    d.run()
    d.outfile.flush()
    d.outfile.close()

    print "DNS servers of subdomain brute" + ' '.join(d.dns_servers)
    #返回第一个dns服务器
    return d.result_lines,d.dns_servers

# 将lijiejie的结果转换成字典
def lijiejie_result_lines(result_lines):
    global DEBUG
    res_resolvtion = dict()

    for item in result_lines:
        tmp_str = item.split("\t")
        tmp_str[0] = tmp_str[0].strip()
        res_resolvtion[tmp_str[0]] = tmp_str[1]


    if DEBUG:
        print "res_resolvtion:  "
        print res_resolvtion

    return res_resolvtion

# 获取riskiq的子域名并且获得riskiq的实例
def call_riskiq(target):
    global DEBUG
    r = riskiq(target,debug=DEBUG)
    r.get_subdomains()

    if DEBUG:
        print "r.subdomains:  "
        print r.subdomains

    return r.subdomains,r

#合并riskiq和lijiejie的子域名
def combine_subdomains(r_subdomains,res,resolver):
    for sub in r_subdomains:
        # 存在就不管了 不存在要添加
        if not sub in res.keys():
            resolve_ip = resolve_name(sub,resolver)
            if resolve_ip == '':
                continue
            else:
                res[sub] = resolve_ip
        else:
            continue

    return res

def resolve_name(domain,resolver):
    #TODO: DNS解析
    # 就那子域名爆破的第一个DNS服务器作为当前的DNS解析
    # 用第一个dns服务器
    try:
        answers = resolver.query(domain)
    except Exception, e:
        print e
        answers = ''

    if answers:
        ips = ', '.join(sorted([answer.address for answer in answers]))
        return ips
    else:
        return ''



def init_resolver(servers):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.lifetime = resolver.timeout = 10.0
    resolver.nameservers = servers

    return resolver

#判断ip出现的次数，并查询反向代理
#出现两次以上的ip，进行反向代理查询
def ip2domain(sub_dict,riskiq_ins,limit=2):
    ips = dict()
    ip_count=0
    reverse_ip = []
    relate_domains = {}

    for ip in sub_dict.values():
        if ip.strip():
            # 多ip的情况
            ip = ip.split(', ')
            for i in ip:
                if i in ips.keys():
                    ips[i] = ips[i] + 1
                else:
                    ips[i] = ip_count+1
        else:
            continue

    if DEBUG:
        print "ips:  "
        print ips
        print "\n"

    for ip in ips.keys():
        if ips[ip] >= limit:
            reverse_ip.append(ip)



    # reverse_ip 需要查询的ip
    if DEBUG:
        print "reverse_ip:  "
        print reverse_ip
        print "\n"

    for ip in reverse_ip:
        reverse_domains = riskiq_ins.get_passive_dns(ip)

        if DEBUG:
            print "reverse_domains:"
            print reverse_domains

        # 该ip是否有解析记录
        if reverse_domains:
            for reverse_domain in reverse_domains:
                # 该域名是否是当前目标的子域
                tmp = reverse_domain.split('.')

                # domain是域 reverse_domain是子域
                if '.'.join(tmp[-2:]) == 'com.cn' or '.'.join(tmp[-2:])== 'net.cn' or tmp[-2] == 'com':
                    domain = '.'.join(tmp[-3:])
                else:
                    domain = '.'.join(tmp[-2:])

                if riskiq_ins.target == domain:
                    if reverse_domain not in sub_dict.keys():
                        sub_dict[reverse_domain] = ip
                    else:
                        continue
                else:
                    if domain in relate_domains.keys():
                        # 如果这个反查的域名就是主域名 example: domain.com => domain.com
                        if reverse_domain == domain:
                            continue

                        # 不重复添加
                        if reverse_domain not in relate_domains[domain]:
                            relate_domains[domain].append(reverse_domain)
                        else:
                            continue
                    else:
                        relate_domains[domain] = [reverse_domain]

        else:
            continue


        if DEBUG:
            print "relate_domains"
            print relate_domains

            print "relate_domains.keys()"
            print [i for i in relate_domains.keys()]
            print "\n"

    return sub_dict,relate_domains

# yandex更新后只能走指定ip，所以只能走代理。
def yandex(query):
    res_num = 0
    url = "https://yandex.com/search/xml?user=whip1ash&key=03.817687278:0a352c9df5dbed29625564671f2010bd&l10n=en&sortby=tm.order%3Dascending&filter=none&groupby=attr%3D%22%22.mode%3Dflat.groups-on-page%3D10.docs-in-group%3D1&lr=*&query=site%3A" + query
    proxy = dict(http='socks5://127.0.0.1:1080', https='socks5://127.0.0.1:1080')
    res = requests.get(url, proxies=proxy, headers={'user-agent': 'curl'})
    # res = requests.get(url, headers={'user-agent': 'curl'})
    xml = res.text
    tree = ET.fromstring(xml.encode('utf8'))
    # ET.tostring(tree,'utf-8','xml')
    response = tree.find('response')
    results = response.find('results')

    if results is None:
        return str(res_num)

    grouping = results[0]

    for ele in grouping.iter(tag='found'):
        if ele.attrib['priority'] == "all":
            res_num = ele.text

    if DEBUG:
        print "Domain = {0} Yandex found {1} results".format(query,res_num)

    return res_num

def find_title(str):
    try:

        title = re.search(r'<title>(.*?)</title>', str, flags=re.IGNORECASE|re.MULTILINE).group(1)

        # 可能存在多title的情况

        in_title = re.search(r'(.*?)</title>',title,flags=re.I|re.M)

        if in_title:
            return in_title.group(1).strip()
        else:
            return title.strip()
    except :
        return False

def get_title(domain):

    # 先发起http请求，如果此站不可达，就不再进行yandex搜索。
    try:
        response = requests.get("http://" + domain, timeout=5)
    except Exception, e:
        # 此站不可达，不在添加到可用的列表中
        return 0
    search_num = yandex(domain)
    length = len(response.text)
    if response.status_code != 404:
        # 彻底解决编码问题

        if find_title(response.text):
            if response.headers['Content-Type'].find("charset=gb2312") > 0:
                response.encoding = 'gb2312'
                text = response.text
                head = find_title(text)
            elif response.headers['Content-Type'].find("charset=gbk") > 0:
                response.encoding = 'gbk'
                text = response.text
                head = find_title(text)
            elif response.text.find("charset=gb2312") > 0:
                text = response.text
                head = find_title(text)
                head = head.encode('latin-1').decode('gbk')
            else:
                response.encoding = 'utf-8'
                text = response.text
                head = find_title(text)

            # 返回 大小 状态码 标题 搜索结果
            return [str(length/1024)+'KB',str(response.status_code),head,search_num]
        else:
            return [str(length/1024)+'KB',str(response.status_code),"no title",search_num]
    else:
        return [str(length/1024)+'KB', str(response.status_code),'404 not found',search_num]


def call_get_title(res_resolvtion,relate_domain):
    # 子域名信息
    s_information = dict()
    # 相关域名信息
    r_information = dict()
    # 初始化reachable变量，默认此站不可达
    reachable = 0
    #需要把res_resolvtion中不可达的站点给剔除掉
    # TODO 这里有点问题 因为目前只是说80端口不可达，并不是完全不可达 所以在在这里需要把解析的域名都给放到nmap进行全端口扫描
    tmp_resolvtion = {}
    tmp_realte_domain  = {}

    for subdomain in res_resolvtion.keys():
        reachable = get_title(subdomain)

        if reachable == 0:
            print subdomain + " is unreachable"
            continue
        else:
            print "Domain = {0} res = {1}".format(subdomain,reachable)

            # 将不可达的域名不放入最终的结果当中
            s_information[subdomain] = reachable
            # 这两个变量名起的不好 应该掉个
            tmp_resolvtion[subdomain] = res_resolvtion[subdomain]

    for r_domain,sr_domain in relate_domain.items():
        for sub_ralate_domain in sr_domain:
            reachable = get_title(sub_ralate_domain)
            if reachable == 0:

                print sub_ralate_domain + " is unreachable"
                continue
            else:
                print "Domain = {0} res = {1}".format(sub_ralate_domain,reachable)

                # 过滤掉不可达
                if tmp_realte_domain.has_key(r_domain):
                    tmp_realte_domain[r_domain].append(sub_ralate_domain)
                else:
                   tmp_realte_domain[r_domain] = [sub_ralate_domain]
                r_information[sub_ralate_domain] = reachable

    return s_information,r_information,tmp_resolvtion,tmp_realte_domain

# 输出结果
def print_result(res_resolvtion,relate_domain,s_infor,r_infor):

    print "\nSubdomains results !!!\n"
    # 输出当前子域名的结果
    for sub in res_resolvtion.keys():
        infor = s_infor[sub]

        if len(infor) == 4:
            size = infor[0]
            code = infor[1]
            head = infor[2]
            search_num = infor[3]

            print u"{0}\t{1}\t{2}\t{3}\t{4}\tYandex found {5} result ".format(sub, res_resolvtion[sub], head, code, size,search_num)
        # This site is unreachable
        else:
            # 不可达的站点在前面已经被过滤
            print "{0}\t{1}\t{2}".format(sub,res_resolvtion[sub],infor[0])

    print "\nRelate domains information !!!!\n"
    for r_domain in relate_domain.keys():
        print r_domain
        # sub relate domain
        for sr_domain in relate_domain[r_domain]:
            information = r_infor[sr_domain]
            if len(information) == 4 :
                size = information[0]
                code = information[1]
                head = information[2]
                search_num = information[3]

                print u"\t{0}\t{1}\t{2}\t{3}\tYandex found {4} result ".format(sr_domain, head, code, size, search_num)
            else:
                print "\t{0}\t{1}".format(sr_domain,information[0])

        print "\n"

def print_domains(resolvtion,relate_domains):
    print "\nHere is subdomains : "
    for sub in resolvtion.keys():
        print u"\t{0}\t{1}".format(sub,resolvtion[sub])

    print "\nHere is relate domains\n"
    for r_domain in relate_domains.keys():
        print "\t"+r_domain+" : "
        for sr_domain in relate_domains[r_domain]:
            print "\t\t"+sr_domain


if __name__ == '__main__':

    DEBUG = True

    target = sys.argv[1]
    res_resolvtion = dict()
    relate_domain = dict()
    subdomain_inform = dict()
    relate_domain_inform = dict()

    result_lines,dns_servers = lijiejie(target)
    res_resolvtion = lijiejie_result_lines(result_lines)
    # print dns_servers
    #获取resolver
    resolver = init_resolver(dns_servers)

    r_subdomains,r = call_riskiq(target)
    combine_subdomains(r_subdomains,res_resolvtion,resolver)

    if DEBUG:
        print res_resolvtion

    res_resolvtion,relate_domain = ip2domain(res_resolvtion,r,limit=5)

    # TODO 通过拿到的res_resolvtion 和 relate_domain 的ip地址，放入队列，让nmap进行扫描。
    # 在这里先输出一次。

    print_domains(res_resolvtion,relate_domain)

    subdomain_inform,relate_domain_inform,res_resolvtion,relate_domain = call_get_title(res_resolvtion,relate_domain)

    print "subdomain_inform"
    print subdomain_inform

    print "relate_domain_inform"
    print relate_domain_inform

    print_result(res_resolvtion,relate_domain,subdomain_inform,relate_domain_inform)


# TEST MAIN
# if __name__ == '__main__':
#     res_resolvtion = {u'tlanding.laohu.com': u'123.196.115.37', u'sdevapi.laohu.com': u'109.244.11.45, 109.244.11.46, 109.244.11.47, 109.244.11.48', u'dac.laohu.com': u'123.196.115.32', u'lhjhd2.games.laohu.com': u'123.196.115.32', u'js.laohu.com': u'123.196.115.32', u'mx01.support.laohu.com': u'118.145.0.15', u'img.games.laohu.com': u'113.142.80.241, 219.145.171.126', u'kf.laohu.com': u'221.228.74.159', u'app.laohu.com': u'113.142.80.242, 124.115.135.187', u'zx.laohu.com': u'113.142.80.242, 124.115.135.187', u'static.games.laohu.com': u'219.144.71.13', u'ff.laohu.com': u'113.142.80.242, 124.115.135.187', u'666.laohu.com': u'123.196.115.32', u'sdxl.laohu.com': u'124.115.135.187', u'event.games.laohu.com': u'221.228.74.250', u'matchbox.laohu.com': u'109.244.11.48', u'bbs.laohu.com': u'221.228.192.66', u'www.laohu.com': u'124.115.135.187', u'dev.laohu.com': u'109.244.11.48', u'laohu.com': u'123.196.115.32', u'lhjhd.games.laohu.com': u'123.196.115.32', u'ops.laohu.com': u'109.244.11.48', u'nq.games.laohu.com': u'113.142.81.223, 219.144.71.13', u'xo.laohu.com': u'123.196.115.37', u'lhj.laohu.com': u'113.142.80.242, 124.115.135.187', u'flzj.laohu.com': u'124.115.135.187', u'wan.laohu.com': u'123.196.115.32', u'sgsy.laohu.com': u'123.196.115.32', u'sm.laohu.com': u'124.115.135.187', u'apidev.laohu.com': u'109.244.11.45, 109.244.11.46, 109.244.11.47, 109.244.11.48', u'event.laohu.com': u'221.228.74.250', u'img.laohu.com': u'113.142.80.242, 124.115.135.187', u'mlbb.laohu.com': u'123.196.115.37', u'hj.laohu.com': u'113.142.80.242, 124.115.135.187', u'yt.laohu.com': u'113.142.80.242, 124.115.135.187', u'log.laohu.com': u'123.196.115.39', u'ads.games.laohu.com': u'120.92.0.222', u'sapi.laohu.com': u'109.244.11.45, 109.244.11.46, 109.244.11.47, 109.244.11.48', u'appcms.laohu.com': u'123.196.115.37', u'pushserver.laohu.com': u'109.244.11.50', u'wl.laohu.com': u'113.142.80.242, 124.115.135.187', u'sd.laohu.com': u'124.115.135.187', u'mad.games.laohu.com': u'120.92.0.222', u'user.laohu.com': u'109.244.11.45, 109.244.11.46, 109.244.11.47, 109.244.11.48', u'bottle.laohu.com': u'109.244.11.48', u'devwiki.laohu.com': u'109.244.11.48', u'inapi.laohu.com': u'109.244.11.48', u'shopapi.laohu.com': u'109.244.11.48', u'vanguard.laohu.com': u'109.244.11.48', u'safestatic.laohu.com': u'109.244.11.45', u'fairy.laohu.com': u'109.244.11.48', u'pushapi.laohu.com': u'109.244.11.49', u'shop.laohu.com': u'109.244.11.48', u'm.laohu.com': u'113.142.80.242, 124.115.135.187', u'support.laohu.com': u'118.145.0.15', u'api.dev.laohu.com': u'109.244.11.46', u'zone.laohu.com': u'109.244.11.48', u's.laohu.com': u'113.142.80.242, 124.115.135.187', u'antifatigue.laohu.com': u'109.244.11.48', u'appserver.laohu.com': u'123.196.115.37', u'i.laohu.com': u'109.244.11.47', u'apkdownload.laohu.com': u'118.213.92.106', u'safestatic.games.laohu.com': u'113.142.80.241, 219.145.171.126'}
#
#     relate_domain = {u'appifan.com': [u'www.appifan.com', u'g.apk.appifan.com'], u'yuekenet.com': [u'wmsj.yuekenet.com'], u'zongheng.com': [u'epub.zongheng.com'], u'wanmei.com': [u'v.wanmei.com', u'member.v.wanmei.com'], u'carry6.com': [u'support.carry6.com'], u'stargame.com': [u'www.stargame.com', u'cmsapi.stargame.com'], u'ifanbox.cn': [u'ifanbox.cn', u'www.ifanbox.cn'], u'178.com': [u'ibook.178.com', u'epub.ibook.178.com', u'app.178.com']}
#
#     subdomain_inform = {u'tlanding.laohu.com': ['0KB', '403', u'403 Forbidden', '0'], u'sdevapi.laohu.com': ['0KB', '200', 'no title', '1'], u'dac.laohu.com': ['3KB', '200', u'\u6e38\u620f\u4e0b\u8f7d -\u300a\u795e\u96d5\u4fa0\u4fa32\u300b\u624b\u6e38\u5b98\u7f51', '0'], u'lhjhd2.games.laohu.com': ['0KB', '404', '404 not found', '0'], u'js.laohu.com': ['3KB', '200', u'\u6e38\u620f\u4e0b\u8f7d -\u300a\u795e\u96d5\u4fa0\u4fa32\u300b\u624b\u6e38\u5b98\u7f51', '0'], u'mx01.support.laohu.com': ['1KB', '404', '404 not found', '0'], u'img.games.laohu.com': ['0KB', '403', u'403 Forbidden', '0'], u'kf.laohu.com': ['13KB', '200', u'\u5ba2\u670d\u4e2d\u5fc3\u9996\u9875', '73'], u'app.laohu.com': ['7KB', '200', u'\u8001\u864e\u6e38\u620f\u5ba2\u6237\u7aef_\u597d\u73a9\u7684\u624b\u673a\u6e38\u620f\u514d\u8d39\u4e0b\u8f7d - \u8001\u864e\u6e38\u620f', '0'], u'zx.laohu.com': ['1KB', '200', u'\u624b\u6e38\u300a\u8bdb\u4ed9\u624b\u6e38\u300b\u5b98\u65b9\u7f51\u7ad9', '7'], u'static.games.laohu.com': ['0KB', '403', u'403 Forbidden', '1'], u'ff.laohu.com': ['27KB', '200', u'\u300a\u6700\u7ec8\u5e7b\u60f3 \u89c9\u9192\u300b\u5b98\u7f51-\u5168CG\u7535\u5f71\u624b\u6e38', '31'], u'666.laohu.com': ['31KB', '200', u'\u91d1\u5eb8\u6b63\u7248\u6388\u6743\u300a\u795e\u96d5\u4fa0\u4fa32\u300b  3D\u6b21\u4e16\u4ee3\u56de\u5408\u624b\u6e38-\u300a\u795e\u96d5\u4fa0\u4fa32\u300b\u624b\u6e38\u5b98\u7f51', '0'], u'sdxl.laohu.com': ['119KB', '200', u'\u300a\u795e\u96d5\u4fa0\u4fa3\u300b\u624b\u6e38\u5b98\u7f51 - \u5b8c\u7f8e\u4e16\u754c\u503e\u60c5\u6253\u9020\u7684\u56de\u5408\u5236\u6b66\u4fa0\u624b\u6e38\uff01', '401'], u'event.games.laohu.com': ['0KB', '403', u'403 Forbidden', '1'], u'matchbox.laohu.com': ['0KB', '404', '404 not found', '0'], u'bbs.laohu.com': ['20KB', '200', u'\u8001\u864e\u6e38\u620f\u8bba\u575b-\u9ad8\u54c1\u8d28\u624b\u673a\u6e38\u620f\u73a9\u5bb6\u793e\u533a-\u624b\u6e38\u7b2c\u4e00\u8bba\u575b -', '207'], u'www.laohu.com': ['27KB', '200', u'\u8001\u864e\u6e38\u620f_\u5b8c\u7f8e\u4e16\u754c\u79fb\u52a8\u6e38\u620f\u5e73\u53f0', '1742'], u'dev.laohu.com': ['0KB', '403', u'403 Forbidden', '33'], u'laohu.com': ['27KB', '200', u'\u8001\u864e\u6e38\u620f_\u5b8c\u7f8e\u4e16\u754c\u79fb\u52a8\u6e38\u620f\u5e73\u53f0', '1742'], u'lhjhd.games.laohu.com': ['0KB', '404', '404 not found', '0'], u'ops.laohu.com': ['0KB', '200', 'no title', '1'], u'nq.games.laohu.com': ['0KB', '200', u'\u624b\u6e38\u300a\u5185\u5d4c\u9875\u300b\u5b98\u65b9\u7f51\u7ad9', '5'], u'xo.laohu.com': ['0KB', '403', u'403 Forbidden', '0'], u'lhj.laohu.com': ['16KB', '200', u'\u300a\u8f6e\u56de\u8bc0\u300b\u624b\u6e38\u5b98\u7f51-\u56fd\u98ce\u4ed9\u7f18RPG\u624b\u6e38-\u8001\u864e\u6e38\u620f', '57'], u'flzj.laohu.com': ['21KB', '200', u'\u300a\u5c01\u9f99\u6218\u7eaa\u300b\u624b\u6e38\u5b98\u65b9\u7f51\u7ad9-\u5c01\u9f99\u6218\u7eaa\u5b98\u7f51-\u5c11\u5973\u4e0e\u9f99\u7684\u76f8\u4f34', '2'], u'wan.laohu.com': ['2KB', '200', u'\u300a\u8d85\u80fd\u5e03\u4e01\u300b\u624b\u6e38\u5b98\u7f51', '28'], u'sgsy.laohu.com': ['35KB', '200', u'\u795e\u9b3c\u4f20\u5947\u5b98\u65b9\u7f51\u7ad9\u2014\u56fd\u6c113D\u9b54\u5e7b\u624b\u6e38', '1'], u'sm.laohu.com': ['17KB', '200', u'\u300a\u795e\u9b54\u5927\u9646\u300b\u624b\u6e38\u5b98\u7f51-\u9884\u7ea6\u5f00\u542f-\u5b88\u62a4\u514b\u5170\u8499\u591a\u5927\u9646\u7684\u8363\u5149', '11'], u'apidev.laohu.com': ['0KB', '200', 'no title', '1'], u'event.laohu.com': ['0KB', '200', u'\u5b8c\u7f8e\u4e16\u754c-\u8001\u864e\u6e38\u620f', '21'], u'img.laohu.com': ['0KB', '403', u'403 Forbidden', '0'], u'mlbb.laohu.com': ['0KB', '403', u'403 Forbidden', '0'], u'hj.laohu.com': ['36KB', '200', u'\u300a\u706b\u70ac\u4e4b\u5149\u300b\u79fb\u52a8\u7248\u5b98\u7f51\u2014\u2014\u706b\u70ac\u4e0d\u7184  \u5192\u9669\u4e0d\u6b62', '122'], u'yt.laohu.com': ['58KB', '200', u'\u300a\u501a\u5929\u5c60\u9f99\u8bb0\u300b- \u91d1\u5eb8\u6b63\u72483DMMO\u624b\u6e38\u625b\u9f0e\u4e4b\u4f5c', '119'], u'log.laohu.com': ['0KB', '403', u'403 Forbidden', '0'], u'ads.games.laohu.com': ['0KB', '404', '404 not found', '0'], u'sapi.laohu.com': ['8KB', '200', u'\u7528\u6237\u767b\u5f55', '0'], u'appcms.laohu.com': ['0KB', '200', 'no title', '0'], u'pushserver.laohu.com': ['0KB', '403', u'403 Forbidden', '0'], u'wl.laohu.com': ['1KB', '200', u'\u300a\u6b66\u6797\u5916\u4f20\u5b98\u65b9\u624b\u6e38\u300b\u5b98\u7f51', '15'], u'sd.laohu.com': ['40KB', '200', u'\u300a\u5c04\u96d5\u82f1\u96c4\u4f203D\u300b\u624b\u6e38\u5b98\u65b9\u7f51\u7ad9', '277'], u'mad.games.laohu.com': ['0KB', '200', 'no title', '1'], u'user.laohu.com': ['8KB', '200', u'\u7528\u6237\u767b\u5f55', '1'], u'bottle.laohu.com': ['0KB', '403', u'403 Forbidden', '0'], u'devwiki.laohu.com': ['0KB', '403', u'403 Forbidden', '0'], u'inapi.laohu.com': ['0KB', '403', u'403 Forbidden', '1'], u'shopapi.laohu.com': ['0KB', '200', 'no title', '0'], u'vanguard.laohu.com': ['0KB', '200', u'Welcome', '0'], u'safestatic.laohu.com': ['0KB', '403', u'403 Forbidden', '0'], u'fairy.laohu.com': ['0KB', '200', 'no title', '0'], u'pushapi.laohu.com': ['0KB', '200', 'no title', '1'], u'shop.laohu.com': ['29KB', '200', u'\u9996\u9875_\u8001\u864e\u5546\u57ce', '28'], u'm.laohu.com': ['38KB', '200', u'\u68a6\u8fb0\u534e\u5178\u2161 8\u670811\u65e5\u76f8\u7ea6\u4e0a\u6d77-\u300a\u68a6\u95f4\u96c6\u300b\u624b\u6e38\u5b98\u65b9\u7f51\u7ad9', '56'], u'support.laohu.com': ['1KB', '404', '404 not found', '0'], u'api.dev.laohu.com': ['0KB', '200', 'no title', '0'], u'zone.laohu.com': ['0KB', '200', 'no title', '0'], u's.laohu.com': ['18KB', '200', u'\u300a\u5c04\u96d5\u82f1\u96c4\u4f20\u300b\u624b\u6e38\u5b98\u65b9\u7f51\u7ad9', '40'], u'antifatigue.laohu.com': ['0KB', '200', 'no title', '0'], u'appserver.laohu.com': ['1KB', '500', u'Error', '0'], u'i.laohu.com': ['8KB', '200', u'\u7528\u6237\u767b\u5f55', '7'], u'apkdownload.laohu.com': ['0KB', '403', u'403 Forbidden', '0'], u'safestatic.games.laohu.com': ['2KB', '403', u'403 Forbidden', '1']}
#
#     relate_domain_inform = {u'www.ifanbox.cn': 0, u'wmsj.yuekenet.com': 0, u'www.appifan.com': 0, u'member.v.wanmei.com': 0, u'epub.ibook.178.com': 0, u'v.wanmei.com': 0, u'support.carry6.com': 0, u'epub.zongheng.com': 0, u'cmsapi.stargame.com': 0, u'g.apk.appifan.com': 0, u'www.stargame.com': 0, u'ibook.178.com': 0, u'ifanbox.cn': 0, u'app.178.com': 0}
#
#     print_result(res_resolvtion, relate_domain, subdomain_inform, relate_domain_inform)

# TEST call_get_title
# if __name__ == '__main__':
#     DEBUG = True
#
#     res_resolvtion = { u'apkdownload.laohu.com': u'118.213.92.106'}
#
#     relate_domain = {u'appifan.com': [u'www.appifan.com', u'g.apk.appifan.com'], u'yuekenet.com': [u'wmsj.yuekenet.com'], u'zongheng.com': [u'epub.zongheng.com'], u'wanmei.com': [u'member.v.wanmei.com', u'v.wanmei.com'], u'carry6.com': [u'support.carry6.com'], u'stargame.com': [u'www.stargame.com', u'cmsapi.stargame.com'], u'178.com': [u'app.178.com', u'ibook.178.com', u'epub.ibook.178.com'], u'ifanbox.cn': [u'ifanbox.cn', u'www.ifanbox.cn']}
#
#     subdomain_inform, relate_domain_inform, res_resolvtion, relate_domain = call_get_title(res_resolvtion,
#                                                                                            relate_domain)
#
#     print_result(res_resolvtion, relate_domain, subdomain_inform, relate_domain_inform)
