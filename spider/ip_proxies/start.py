# -*- coding: utf-8 -*-
# @Author: lzc
# @Time  :2019/8/23

"""
高匿：服务器不知道我们使用了代理。
普匿：服务器知道我们使用了代理，但一般无法查出我们的IP地址。
透明：服务器知道我们使用了代理，且能查出你的IP地址。（本IP池不收集）
"""

from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ip_proxies.spiders.kuaidaili import KuaidailiSpider
from ip_proxies.spiders.jiangxianli import JiangxianliSpider

# 测试爬虫时使用，默认注释掉
# cmdline.execute('scrapy crawl verify'.split())

# 在同一进程同时运行多个爬虫
process = CrawlerProcess(get_project_settings())
process.crawl(KuaidailiSpider)
process.crawl(JiangxianliSpider)
# 脚本将会停在此处知道所有爬虫完成
process.start()
# process.stop()
