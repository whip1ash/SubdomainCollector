# -*- coding:utf-8 -*-

import sys

# 通过ip来排序域名，这样可以看出大概的ip范围，然后确定反代网关，确定生产段 暂时废弃

def read_file(r_path):
	f_read = open(r_path,'r')
	res = []

	for line in f_read:
		res.append(line)

	f_read.close()

	return res


def write_file(w_path,res_list):
	w_open = open(w_path,'w')
	for i in res_list:
		w_open.write(i+"\n")

	w_open.close()

def str_sort(param_list):
	res = []
	for i in param_list:

		tmp = i.split(' ',1)
		res.append(tmp[1].strip()+"    "+tmp[0])
	res.sort()
	return res

if __name__ == '__main__':
    r_path = sys.argv[1]
    o_path = sys.argv[2]

    pre = read_file(r_path)
    res = str_sort(pre)

    for i in res:
		print i
    write_file(o_path,res)


