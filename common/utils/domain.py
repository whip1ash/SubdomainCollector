#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys

# 域名去重 暂时废弃

if __name__ == "__main__":
	read_path = sys.argv[1]
	
	domains = []
	f_read = open(read_path,'r')
	
	for line in f_read:
		domains.append(line)
		
	f_read.close()
	
	domains = list(set(domains))
	domains.sort()
	
	for i in domains:
		print i