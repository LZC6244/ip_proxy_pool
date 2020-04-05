# -*- coding: utf-8 -*-
import os
from datetime import datetime

# Scrapy settings for ip_proxies project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ip_proxies'

SPIDER_MODULES = ['ip_proxies.spiders']
NEWSPIDER_MODULE = 'ip_proxies.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'ip_proxies (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1.5
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'ip_proxies.middlewares.IpProxiesSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'ip_proxies.middlewares.IpProxiesDownloaderMiddleware': 543,
    'ip_proxies.middlewares.RandomUA': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     'ip_proxies.pipelines.IpProxiesPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 3
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 重试次数设置 （默认为2）
RETRY_TIMES = 2
# 超时时间设为10 （默认180）
DOWNLOAD_TIMEOUT = 10

TEST_URLS = [
    'https://www.baidu.com',
    'https://cn.bing.com/',
    'https://www.so.com/',
]

# 日志文件设置
LOG_LEVEL = 'DEBUG'
# LOG_LEVEL = 'WARNING'
LOG_ENCODING = 'utf-8'
DATE = datetime.now()
os.makedirs(os.path.join(os.path.dirname(__file__), 'log'), exist_ok=True)
TIME_FORMAT = '%Y-%m-%dT%H_%M_%S'
LOG_FILE = f'log/{DATE.strftime(TIME_FORMAT)}.log'

# 不需要去重 2019.8.23
# # 使用scrapy-redis里的去重组件，不使用scrapy默认的去重
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# # 使用scrapy-redis里的调度器组件，不实用scrapy默认的调度器
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# # 允许暂停，redis请求记录不丢失
# SCHEDULER_PERSIST = True
# REDIS_HOST = '127.0.0.1'
# # REDIS_HOST = '139.9.58.217'
# REDIS_PORT = 6379
# REDIS_PARAMS = {'password': 'xxxxx'}


USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 '
    'Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
]

# IP_PROXY 相关 URL 配置
GET_CSRF = 'http://127.0.0.1:8000/ip_proxy/get_csrf/'
LIST_PROXY = 'http://127.0.0.1:8000/ip_proxy/list/?page=1'
GET_PROXY = 'http://127.0.0.1:8000/ip_proxy/get/'
UPDATE_PROXY = 'http://127.0.0.1:8000/ip_proxy/update/'
DEL_PROXY = 'http://127.0.0.1:8000/ip_proxy/del/'
