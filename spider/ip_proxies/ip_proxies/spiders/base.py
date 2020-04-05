# -*- coding: utf-8 -*-
import ast
import scrapy
from scrapy import Request, FormRequest
from datetime import datetime
from ip_proxies.settings import GET_CSRF, UPDATE_PROXY, TIME_FORMAT

"""
爬虫爬取代理后，将代理上传到数据库的模板
"""


class BaseSpider(scrapy.Spider):
    name = 'base'

    # allowed_domains = ['base_spider']
    # start_urls = ['http://base_spider/']

    def start_requests(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip,deflate,br'
        }
        for url in self.start_urls:
            request = Request(url=url, headers=self.headers, callback=self.parse)
            yield request

    def parse(self, response):
        pass

    def verify_porxy(self, response):
        # 能进来解析响应就说明该代理能用
        # with open('test.html', 'wb') as f:
        #     f.write(response.body)
        item = response.meta['item']
        # 最后验证时间
        date = datetime.strftime(datetime.now(), TIME_FORMAT)
        # date = datetime.strptime(date, TIME_FORMAT)
        item['verify_time'] = date
        url = GET_CSRF
        request = Request(url=url, callback=self.update_proxy, dont_filter=True)
        request.meta['item'] = item
        yield request

    def update_proxy(self, response):
        # 该响应的请求地址须为：GET_CSRF
        # 此时的 item 须以含有代理相关信息
        item = response.meta['item']
        csrf = ast.literal_eval(response.text).get('csrf')
        url = UPDATE_PROXY
        formdata = {
            'csrfmiddlewaretoken': csrf,
            'ip': item.get('ip'),
            'port': item.get('port'),
            'anonymity': item.get('anonymity', ''),
            'net_type': item.get('net_type', ''),
            'ip_location': item.get('ip_location', ''),
            'verify_time': item.get('verify_time'),
        }
        # 此处须指明一个回调函数，即使我们什么也不需要做
        # 若是不指定回调，scrapy 将把 parse 方法作为回调函数
        # 若继承本爬虫的其他爬虫重写了 parse 方法，将有几率导致发生我们意料之外的错误
        # see https://docs.scrapy.org/en/latest/topics/request-response.html?highlight=callback#request-objects
        request = FormRequest(url=url, formdata=formdata, callback=self.verify_end, dont_filter=True)
        return request

    def verify_end(self, response):
        # do nothing
        pass
