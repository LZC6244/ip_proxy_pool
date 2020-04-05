# -*- coding: utf-8 -*-
import random
import scrapy
from scrapy import Request
from ip_proxies.spiders.base import BaseSpider
from ip_proxies.items import IpProxiesItem
from ip_proxies.settings import TEST_URLS, LOG_FILE


class JiangxianliSpider(BaseSpider):
    name = 'jiangxianli'
    # allowed_domains = ['jiangxianli.com']
    start_urls = ['http://ip.jiangxianli.com/?page=1']

    custom_settings = {
        'LOG_FILE': LOG_FILE.replace('log/', f'log/{name}__', 1),

    }

    def parse(self, response):
        # print(response.url)
        # 每一页的代理 ip 信息列表
        ip_info_li = response.xpath('//table[@class="table table-hover table-bordered table-striped"]/tbody//tr')
        # IP PORT 匿名度 类型 的列表
        title_li = ['ip', 'port', 'anonymity', 'net_type']
        for i in ip_info_li:
            item = IpProxiesItem()
            td_li = i.xpath('./td/text()').getall()
            # 该网站只有 "高匿" "透明" 两种分类
            # 我们不需要 "透明" , 去除
            if td_li[3] in '透明':
                continue
            for k, v in zip(title_li, td_li[1:5]):
                item[k] = v
            # td_li[5] -> 中国 广东 汕尾
            # td_li[6] -> 联通
            # 二者合在一起才是所需数据
            item['ip_location'] = ' '.join(td_li[5:7]) if len(td_li) == 12 else ''
            if not item['net_type']:
                item['net_type'] = 'HTTP'
            # 从上述数据组合代理为如下格式 ：http://some_proxy_server:port
            proxy = item['net_type'].lower() + '://' + item['ip'] + ':' + item['port']
            # 需加 dont_filter=True 因为测试代理是否可用每次都是访问固定的几个页面来测试
            request = Request(url=random.choice(TEST_URLS), headers=self.headers,
                              meta={'proxy': proxy, 'item': item},
                              callback=self.verify_porxy, dont_filter=True)
            yield request

        # 该网站页数不固定，可能为为 2~3 页或更多页
        # 此处通过是否仍能点击下一页判断
        if_next = response.xpath('//ul[@class="pagination"]/li')
        if if_next:
            if_next = if_next[-1]
            if not if_next.xpath('./@class'):
                next_url = if_next.xpath('./a/@href').get()
                next_request = Request(url=next_url, callback=self.parse, dont_filter=True)
                yield next_request
