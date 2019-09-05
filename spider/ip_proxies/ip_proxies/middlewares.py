# -*- coding: utf-8 -*-
import random
import requests
from twisted.internet.error import TimeoutError
from ip_proxies.settings import USER_AGENTS, GET_CSRF, GET_PROXY, DEL_PROXY
# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

session = requests.session()
csrf = session.get(GET_CSRF).json().get('csrf')


def get_proxy():
    return requests.get(GET_PROXY).json()


def del_proxy(ip, port):
    return session.post(DEL_PROXY, {'csrfmiddlewaretoken': csrf, 'ip': ip, 'port': port})


class IpProxiesSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class IpProxiesDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUA(object):

    def process_request(self, request, spider):
        # print('*' * 50)

        user_agent = random.choice(USER_AGENTS)
        # print(user_agent)
        request.headers['User-Agent'] = user_agent


class IpProxyMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENTS)
        request.headers['User-Agent'] = ua
        if request.meta.get('retry_times'):
            # request.meta['proxy'] = request.meta['proxy']
            pass
        else:
            proxy_json = get_proxy()
            request.meta['proxy'] = proxy_json.get('proxy')
            request.meta['ip_proxy'] = proxy_json.get('ip')
            request.meta['port_proxy'] = proxy_json.get('port')

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            del_proxy(request.meta['ip_proxy'], request.meta['port_proxy'])
        return request.copy()
