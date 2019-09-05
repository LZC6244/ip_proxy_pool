# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IpProxiesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()['ip', 'port', 'anonymity', 'type', 'location']

    ip = scrapy.Field()
    port = scrapy.Field()
    # 匿名度：高匿、普通（也只爬取这两种，透明类型的不要）
    anonymity = scrapy.Field()
    # HTTP OR HTTPS
    net_type = scrapy.Field()
    # 代理 IP 的位置
    ip_location = scrapy.Field()
    # 最后验证时间
    verify_time = scrapy.Field()
