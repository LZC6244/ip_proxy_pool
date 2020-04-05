# -*- coding: utf-8 -*-
import random
from scrapy import Request
from ip_proxies.spiders.base import BaseSpider
from ip_proxies.items import IpProxiesItem
from ip_proxies.settings import TEST_URLS, LOG_FILE


class XicidailiSpider(BaseSpider):
    name = 'xicidaili'
    # allowed_domains = ['xicidaili.com']
    # 只爬取前三页，免费代理质量不高
    start_urls = ['https://www.xicidaili.com/nn/%s/' % x for x in range(1, 4)]
    custom_settings = {
        'LOG_FILE': LOG_FILE.replace('log/', f'log/{name}__', 1),
    }

    def parse(self, response):
        # 每一页的代理 ip 信息列表
        ip_info_li = response.xpath('//table[@id="ip_list"]//tr[@class]')
        # IP PORT 位置 匿名度 类型
        title_li = ['ip', 'port', 'ip_location', 'anonymity', 'net_type']
        for i in ip_info_li:
            item = IpProxiesItem()
            for k, v in zip(title_li, i.xpath('./td')[1:6]):
                item[k] = v.xpath('string(.)').get().strip()
            # 从上述数据组合代理为如下格式 ：http://some_proxy_server:port
            proxy = item['net_type'].lower() + '://' + item['ip'] + ':' + item['port']
            # 需加 dont_filter=True 因为测试代理是否可用每次都是访问固定的几个页面来测试
            request = Request(url=random.choice(TEST_URLS), headers=self.headers,
                              meta={'proxy': proxy, 'item': item},
                              callback=self.verify_porxy, dont_filter=True)
            yield request
