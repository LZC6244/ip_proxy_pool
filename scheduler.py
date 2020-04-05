# -*- coding: utf-8 -*-
# @Author: lzc
# @Time  : 2019/9/9
import os
import subprocess
from datetime import datetime, timedelta
from runpy import run_path
from apscheduler.schedulers.blocking import BlockingScheduler

from rm_log import rm_log

project_path = os.path.dirname(__file__)
server_path = os.path.join(project_path, 'ip_proxy_site')
spider_path = os.path.join(project_path, 'spider', 'ip_proxies')
log_path = os.path.join(spider_path, 'log')


def enable_crawl_spider():
    os.chdir(spider_path)
    subprocess.run('python start.py')


def enable_verify_spider():
    os.chdir(spider_path)
    subprocess.run('python start_verify.py')


def enable_server():
    os.chdir(server_path)
    subprocess.run('python manage.py runserver 0.0.0.0:8000')


def remove_log():
    settings = os.path.join(spider_path, 'ip_proxies', 'settings.py')
    settings = run_path(settings)
    time_format = settings.get('TIME_FORMAT')
    rm_log(log_path, time_format)


# enable_crawl_spider()
sched = BlockingScheduler()
sched.add_job(enable_server, name='Django server')
sched.add_job(enable_crawl_spider, 'interval', hours=4, next_run_time=datetime.now() + timedelta(seconds=10),
              name='定时代理爬取')
sched.add_job(enable_verify_spider, 'interval', hours=2, name='定时代理有效性验证')
sched.add_job(remove_log, 'interval', days=2, name='定时删除2天前的日志文件')
sched.start()
