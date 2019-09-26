# -*- coding: utf-8 -*-
import re
import random
from scrapy import Request
from ip_proxies.spiders.base import BaseSpider
from ip_proxies.items import IpProxiesItem
from ip_proxies.settings import TEST_URLS, LOG_FILE


class Ip3366Spider(BaseSpider):
    name = 'ip3366'
    # allowed_domains = ['ip3366']
    # 爬取云代理的高匿、普匿代理各前三页
    # 高匿
    start_urls = ['http://www.ip3366.net/free/?stype=1&page=%s' % x for x in range(1, 4)]
    # 普匿
    start_urls += ['http://www.ip3366.net/free/?stype=2&page=%s' % x for x in range(1, 4)]
    custom_settings = {
        'LOG_FILE': LOG_FILE.replace('.log', '__%s.log' % name)
    }

    def parse(self, response):
        stype = re.findall('stype=(\d)&', response.url)[0]
        # 每一页的代理 ip 信息列表
        ip_info_li = response.xpath('//table[@class="table table-bordered table-striped"]/tbody//tr')
        anonymity = '高匿' if stype == '1' else '普匿'
        # IP PORT 匿名度 类型 位置 的列表
        title_li = ['ip', 'port', 'anonymity', 'net_type', 'ip_location']
        for i in ip_info_li:
            item = IpProxiesItem()
            content_li_raw = i.xpath('./td/text()').getall()[:5]
            # ip port
            content_li = content_li_raw[:2]
            net_type = content_li_raw[3]
            ip_location = content_li_raw[4].split('_')[-1]
            content_li += [anonymity, net_type, ip_location]
            for k, v in zip(title_li, content_li):
                item[k] = v
            # 从上述数据组合代理为如下格式 ：http://some_proxy_server:port
            proxy = item['net_type'].lower() + '://' + item['ip'] + ':' + item['port']
            print(proxy)
            # 需加 dont_filter=True 因为测试代理是否可用每次都是访问固定的几个页面来测试
            request = Request(url=random.choice(TEST_URLS), headers=self.headers,
                              meta={'proxy': proxy, 'item': item},
                              callback=self.verify_porxy, dont_filter=True)
            yield request
