# SubdomainCollector
Personal Subdomain Recon Tools 

本工具整合了lijiejie子域名爆破和riskiq的接口，并且结合日常的经验整合了Yandex的API接口。

## 具体流程如下：
1. 使用lijiejie对提供的域名进行子域名爆破。
2. 使用RISKIQ进行子域名查询。
3. 对RISKIQ查询的域名进行DNS解析，删除没有DNS记录的，将结果与1.结果合并。
4. 统计IP的出现次数，超过limit次则判断为反向代理。
5. 调用RISKIQ的接口，查询反向代理的IP绑定的域名。
6. 判断反向代理绑定的域名是否是目标域，否则为相关域。
7. 对上述流程后得到的域名进行HTTP请求，并使用Yandex进行搜索，以便判断该域名下是否存在一定的业务。

## 使用指南：
1. RISKIQ
账号注册地址 
https://community.riskiq.com/registration

API查看地址 
https://community.riskiq.com/settings  - API ACCESS

2. Yandex
Yandex更新后每个账号只允许一个IP进行API的调用，所以我使用了代理，Yandex的请求同一使用代理服务器进行请求。

账号注册地址
https://passport.yandex.com/registration

Yandex IP设置地址
https://xml.yandex.com/settings/

## TODO: 
- [ ] 整体流程优化。
- [ ] 代码重构，各个部分拆成模块，控制主流程。
- [ ] 引入外部参数，使用argparse。
- [ ] 需要在判断是否为反代的流程中加入判断是否为CDN。
- [ ] 判断一个C段内的IP频率
- [ ] 引入NMAP扫描
- [ ] 添加模块，通过ASN或者IP段批量请求IP的443端口，获取CN证书。
