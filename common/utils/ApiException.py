#!/usr/bin/env python
# encoding: utf-8

'''
@author: whip1ash
@contact: security@whip1ash.cn
@software: pycharm 
@file: YandexException.py
@time: 2019/9/21 15:57
@desc:
'''

class ApiException(Exception):
    def __init__(self,moudle,code=0,info="未知Yandex错误"):
        error = "{} occurred an error, code = {} ,info = '{}'".format(moudle,code,info)
        Exception.__init__(self,error)


if __name__ == '__main__':
    try:
        raise ApiException(0,"qqqqqq exception")
    except ApiException as e :
        print e.message
