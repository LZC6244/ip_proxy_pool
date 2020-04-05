# -*- coding: utf-8 -*-
# @Author: lzc
# @Time  : 2019/9/26
import os
from datetime import datetime, timedelta


def rm_log(path, time_format):
    file_li = os.listdir(path)
    for i in file_li:
        # 当前日期
        date_now = datetime.now()
        # 日志文件的日期
        date_log = i.split('__')[0]
        date_log = date_log.replace('.log', '')
        date_log = datetime.strptime(date_log, time_format)
        # 二者相差的天数
        day = (date_now - date_log).days
        # 删除 2 天前的日志文件
        if day >= 2:
            os.remove(os.path.join(path, i))
