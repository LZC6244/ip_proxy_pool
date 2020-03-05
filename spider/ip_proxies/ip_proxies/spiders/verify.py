# -*- coding: utf-8 -*-
import re
import random
import scrapy
from scrapy import Request

from ip_proxies.items import IpProxiesItem
from ip_proxies.spiders.base import BaseSpider
from ip_proxies.settings import LIST_PROXY, TEST_URLS, DOWNLOADER_MIDDLEWARES, LOG_FILE


class VerifySpider(BaseSpider):
    name = 'verify'
    # allowed_domains = ['verify']
    start_urls = [LIST_PROXY]
    DOWNLOADER_MIDDLEWARES['ip_proxies.middlewares.ManageProxy'] = 150

    custom_settings = {
        'LOG_FILE': LOG_FILE.replace('.log', '__%s.log' % name),
        # 下面三行设置该爬虫为 BFO
        'DEPTH_PRIORITY': 1,
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
        # 启用中间件
        'DOWNLOADER_MIDDLEWARES': DOWNLOADER_MIDDLEWARES
    }
    proxy_info = []

    def parse(self, response):
        # 本次只获取代理共有几页
        # 总页数
        total_page = response.xpath('string(//p[1])').get()
        total_page = int(re.findall('\d+', total_page)[-1])
        # 如 'http://127.0.0.1:8000/ip_proxy/list/?page='
        url_1 = re.findall('.*page=', LIST_PROXY)[0]
        # 页数 URL 列表，如 'http://127.0.0.1:8000/ip_proxy/list/?page=1' 'http://127.0.0.1:8000/ip_proxy/list/?page=2' ...
        page_li = [url_1 + str(x) for x in range(1, total_page + 1)]
        for url in page_li:
            request = Request(url=url, callback=self.parse_list, meta={'total_page': total_page}, dont_filter=True)
            yield request

    def parse_list(self, response):
        total_page = response.meta['total_page']
        proxy_li = response.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
        for p in proxy_li:
            # tmp_li=[ip,port,net_type]
            net_type = p.xpath('./td[3]/text()').get()
            if not net_type:
                net_type = 'HTTP'
            tmp_li = [p.xpath('./td[1]/text()').get(), p.xpath('./td[2]/text()').get(), net_type]
            self.proxy_info.append(tmp_li)
        # 获取完所有代理再进行代理验证
        if len(self.proxy_info) > (total_page - 1) * 20:
            for p_info in self.proxy_info:
                item = IpProxiesItem()
                item['ip'] = p_info[0]
                item['port'] = p_info[1]
                item['net_type'] = p_info[2]
                proxy = item['net_type'].lower() + '://' + item['ip'] + ':' + item['port']
                print('正在验证：%s' % proxy)
                request = Request(url=random.choice(TEST_URLS), headers=self.headers,
                                  meta={'proxy': proxy, 'item': item}, callback=self.verify_porxy, dont_filter=True)
                yield request
