# -*- coding: utf-8 -*-
# @Author: lzc
# @Time  : 2019/9/9
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

project_path = os.path.abspath('.')
server_path = os.path.join(project_path, 'ip_proxy_site')
spider_path = os.path.join(project_path, 'spider', 'ip_proxies')


def enable_crawl_spider():
    os.chdir(spider_path)
    os.system('python start.py')


def enable_verify_spider():
    os.chdir(spider_path)
    os.system('scrapy crawl verify')


def enable_server():
    os.chdir(server_path)
    os.system('python manage.py runserver')


sched = BlockingScheduler()
sched.add_job(enable_server, name='Django server')
# 设置了运行间隔后，第一次运行需等待间隔时间
# 故在此处需要加入一个初始运行任务
# sched.add_job(enable_crawl_spider, name='初始代理爬取')
sched.add_job(enable_crawl_spider, 'interval', hours=4, next_run_time=datetime.now() + timedelta(seconds=10),
              name='定时代理爬取')
sched.add_job(enable_verify_spider, 'interval', hours=2, name='定时代理有效性验证')
sched.start()
