#!/usr/bin/python
# -*- coding:utf-8 -*-
import whois
import sys
import json

	# 检查域名不同的后缀是否是一个企业



def whois_local(domain):
	return whois.whois(domain)
	
if __name__ == "__main__":
	suffixs = []
	domain = sys.argv[1]
	keyword = sys.argv[2]

	f_read = open('dir.txt','r')
	
	for line in f_read:
		line = line.strip()
		suffixs.append(line)

	f_read.close()

	email = ''
	res = ''

	for i in suffixs:
		tmp = domain + i

		try:
			res = whois_local(tmp)

		except Exception as e:
			print tmp+"\t"+str(e)

		if not res:
			continue

		email = res.emails

		if not email:
			continue

		if (type(email)==list):
			for i in email:
				if(i.find(keyword) != -1):
					print tmp+"\t"+email
					continue
		else:
			if (email.find(keyword) != -1):
				print tmp+"\t"+ email

		res = ''
		email = ''
	# try:
	# 	whois_local("jianqi.vip")
	#
	# except Exception as e:
	# 	print e

