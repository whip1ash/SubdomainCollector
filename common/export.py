#!/usr/bin/python
# -*- coding: utf-8 -*-
import logger


def write_data(fpath,data):
    """
    导出数据，返回 Null(以 w 模式)
    :param fpath: 输出的文件路径
    :param data: 输出的数据
    :return: NULL
    """
    try:
        with open(fpath,"w",encoding="utf8") as file:
            file.write(data)
            logger.logger("导出数据").info("导出成功")
    #假如是二进制数据
    except TypeError :
        with open(fpath,"wb") as file:
            file.write(data)
            logger.logger("导出数据").info("导出成功")
    except Exception as e:
        logger.logger("导出数据").error("导出失败：" + str(e))

def append_data(fpath,data):
    """
    追加数据，返回 Null(以 a+ 模式)
    :param fpath: 输出的文件路径
    :param data: 输出的数据，数据前会加上\n
    :return: NULL
    """
    try:
        with open(fpath, "a+") as file:
            file.write("\n"+data)
            logger.logger("追加数据").info("追加成功")
    except Exception as e:
        logger.logger("追加数据").error("追加失败：" + str(e))




if __name__ == '__main__':
    fpath = "1.txt"
    data = "123"
    data2 = "456"
    write_data(fpath,data)
    append_data(fpath,data2)




