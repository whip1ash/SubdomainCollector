#!/usr/bin/python
# -*- coding: utf-8 -*-
import coloredlogs
import logging

def logger(name):
    """
    日志工具文件
    :param name: 模块名
    :return: logger对象
    """

    coloredlogs.DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    coloredlogs.DEFAULT_DATE_FORMAT = "%H:%M:%S"

    logger = logging.getLogger(name)

    coloredlogs.install(level="DEBUG",logger=logger)
    return logger



if __name__ == '__main__':
    logger("").info("info")
    logger("").debug("debug")
    logger("").error("error")
    logger("").fatal("fatal")







