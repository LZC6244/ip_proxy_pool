# -*- coding: utf-8 -*-
# @Author: lzc
# @Time  : 2019/9/26
import os
import re
from datetime import datetime, timedelta


def rm_log(path, time_format):
    if not os.path.exists(path):
        return 'path not exists.'
    # 当前日期
    date_now = datetime.now()
    file_li = os.listdir(path)
    for i in file_li:
        # 日志文件的日期
        date_log = re.findall('\d{4}-\d{2}-\d{2}T\d{2}_\d{2}_\d{2}', i)
        if not date_log:
            continue
        date_log = date_log[0]
        date_log = datetime.strptime(date_log, time_format)
        # 二者相差的天数
        day = (date_now - date_log).days
        # 删除 2 天前的日志文件
        if day >= 2:
            os.remove(os.path.join(path, i))
