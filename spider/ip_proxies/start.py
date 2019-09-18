# -*- coding: utf-8 -*-
# @Author: lzc
# @Time  :2019/8/23


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
