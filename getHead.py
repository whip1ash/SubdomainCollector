# -*- coding:utf-8 -*-
import requests
import sys
import re
import xml.etree.ElementTree as ET


def find_title(str):
	try:
		title = re.search(r'<title>(.*?)</title>', str, flags=re.IGNORECASE|re.MULTILINE).group(1)
		return title.strip()
	except :
		return False


# yandex 这里还需要指定ip，所以只能走代理，是固定的ip地址 124.156.117.48 香港的vps
def yandex(query):
	res_num = 0

	url = "https://yandex.com/search/xml?user=whip1ash&key=03.817687278:0a352c9df5dbed29625564671f2010bd&l10n=en&sortby=tm.order%3Dascending&filter=none&groupby=attr%3D%22%22.mode%3Dflat.groups-on-page%3D10.docs-in-group%3D1&lr=*&query=site%3A" + query
	res = requests.get(url, headers={'user-agent': 'curl'},proxies=dict(http='socks5://127.0.0.1:1080',https='socks5://127.0.0.1:1080'))
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
	return res_num

file = sys.argv[1]

# print file
# for i in open("hichina.txt"):
for i in open(file):
	try:
		a = i.strip()
		b = a  # [0:-1] #实验发现linux下才需要这一步，windows下不需要
		# print b

		search_num = yandex(b)

		response = requests.get("http://" + b, timeout=5)

			# response.encoding='utf-8'

		length = len(response.text)

		if response.status_code != 404:
			#彻底解决编码问题

			if find_title(response.text) :
				if response.headers['Content-Type'].find("charset=gb2312")>0:
					response.encoding = 'gb2312'
					text = response.text
					head = find_title(text)
				elif response.headers['Content-Type'].find("charset=gbk") > 0:
					response.encoding = 'gbk'
					text = response.text
					head = find_title(text)
				elif response.text.find("charset=gb2312") > 0 :
					text = response.text
					head = find_title(text)
					head = head.encode('latin-1').decode('gbk')
				else:
					response.encoding='utf-8'
					text = response.text
					head = find_title(text)

				result = '\033[0;32m' + b + '     ' + str(length / 1024) + 'KB     ' + str(response.status_code) + '     ' + head + '     '+"Yandex found " +search_num+" result"+'\033[0m'
				print result
			else:
				result = '\033[0;36m' + b + '     ' + str(length / 1024) + 'KB     ' + str(response.status_code) + '     no title' +  '     '+"Yandex found " +search_num+" result"+'\033[0m'
				print result

		# elif response.status_code == 404 or response.status_code == 403:
		# 	search_num = yandex(i)
		#
		# 	if search_num == 0:


		else:
			result = b + '     ' + str(length / 1024) + 'KB     ' + str(response.status_code)+ '     '+"Yandex found " +search_num+" result"
			print result

	except Exception, e:
		# print e.message

		result = '\033[1;32m' + b + '\033[0m'
		print result

		pass