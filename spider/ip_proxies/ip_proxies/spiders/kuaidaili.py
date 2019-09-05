# -*- coding: utf-8 -*-
import random
from scrapy import Request
from ip_proxies.spiders.base import BaseSpider
from ip_proxies.items import IpProxiesItem
from ip_proxies.settings import TEST_URLS

"""
1.不计算响应时间，因为 scrapy 是异步发送请求的
"""


class KuaidailiSpider(BaseSpider):
    name = 'kuaidaili'
    # allowed_domains = ['www.kuaidaili.com']
    # 只爬取前三页的就够了，免费代理质量不高
    start_urls = ['https://www.kuaidaili.com/free/inha/%s/' % x for x in range(1, 4)]

    # start_urls = ['https://www.kuaidaili.com/free/inha/2/']

    def parse(self, response):
        # print(response.url)
        # 每一页的代理 ip 信息列表
        ip_info_li = response.xpath('//table[@class="table table-bordered table-striped"]/tbody//tr')
        # IP PORT 匿名度 类型 位置 的列表
        title_li = ['ip', 'port', 'anonymity', 'net_type', 'ip_location']
        for i in ip_info_li:
            item = IpProxiesItem()
            for k, v in zip(title_li, i.xpath('./td/text()').getall()[:5]):
                item[k] = v
            # 此网站爬取的都是高匿代理，但其名称为"高匿名"，先将其统一为"高匿"
            item['anonymity'] = '高匿'
            # 从上述数据组合代理为如下格式 ：http://some_proxy_server:port
            proxy = item['net_type'].lower() + '://' + item['ip'] + ':' + item['port']
            # 需加 dont_filter=True 因为测试代理是否可用每次都是访问固定的几个页面来测试
            request = Request(url=random.choice(TEST_URLS), headers=self.headers,
                              meta={'proxy': proxy, 'item': item},
                              callback=self.verify_porxy, dont_filter=True)
            yield request
