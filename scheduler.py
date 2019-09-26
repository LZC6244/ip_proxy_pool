# -*- coding: utf-8 -*-
# @Author: lzc
# @Time  : 2019/9/9
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

from rm_log import rm_log

project_path = os.path.abspath('.')
server_path = os.path.join(project_path, 'ip_proxy_site')
spider_path = os.path.join(project_path, 'spider', 'ip_proxies')
log_path = os.path.join(spider_path, 'log')


def enable_crawl_spider():
    os.chdir(spider_path)
    os.system('python start.py')


def enable_verify_spider():
    os.chdir(spider_path)
    os.system('python start_verify.py')


def enable_server():
    os.chdir(server_path)
    os.system('python manage.py runserver 0.0.0.0:8000')


def remove_log():
    rm_log(log_path)


sched = BlockingScheduler()
sched.add_job(enable_server, name='Django server')
sched.add_job(enable_crawl_spider, 'interval', hours=4, next_run_time=datetime.now() + timedelta(seconds=10),
              name='定时代理爬取')
sched.add_job(enable_verify_spider, 'interval', hours=2, name='定时代理有效性验证')
sched.add_job(remove_log, 'calendarinterval', days=1, name='定时删除2天前的日志文件')
sched.start()
