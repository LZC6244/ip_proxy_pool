# 基于 Django2 和 Scrapy 的 IP 代理池
## 介绍
- 版本：![](https://img.shields.io/badge/Python-3.x-brightgreen) ![](https://img.shields.io/badge/Django-2.x-brightgreen)
- 本项目是一个使用 Django 作为接口后端，scrapy 作为爬虫的一个代理 IP 池。
- 数据库：sqlite 免去安装数据库烦恼（亦可使用其他 Django 支持的数据库，更改 Django settings 文件即可）
- 启动程序后，首先会启动 Django 服务器，然后进行第一次的代理爬取，稍等几分钟即可看见代理陆续入库。
- 测试地址：[测试地址](http://139.9.58.217:8000/ip_proxy/list/) 请勿压测 影响正常使用则关闭测试地址
### 代理说明
- 高匿：服务器不知道我们使用了代理。
- 普匿：服务器知道我们使用了代理，但一般无法查出我们的IP地址。
- 透明：服务器知道我们使用了代理，且能查出你的IP地址。（本 IP 池不收集）
### 响应时间说明
- 不计算响应时间，因为 scrapy 是`异步`发送请求的
### 代理验证说明
- 每 `4` 个小时从代理网站爬取一次代理
- 每 `2` 个小时验证一次代理池中的全部代理
- 若时间间隔到了 `爬取/验证` 代理未完成，则会等待其完成再进行 `爬取/验证` 代理动作
- 爬取到新的代理时 `priority` 设为 `2` 
- 代理验证成功时 `priority` 加 `1`
- 代理验证失败时 `priority` 减 `1` ，`priority` 为 `0` 则删除该代理
## 环境需求
在本项目路径下执行命令：
```shell script
pip install -r requirements.txt
```
## 启动代理池
在本项目路径下执行命令：
```shell script
pthon scheduler.py
```
若是将本项目部署在云主机之类的，通过 `ssh` 操控  
为了避免 `session` 断开则程序中断，可以使用以下命令：
```shell script
nohup pthon scheduler.py &
```
- 若在 `Ubuntu` 中使用，可将本代理池注册成服务。  
- 方法请看[这里](https://github.com/LZC6244/ip_proxy_pool/blob/master/docs/Ubuntu_service.md)
## 在爬虫中使用本代理池
以 scrapy 为例。  
非本地情况下，IP 地址更换为本项目实际 IP 地址即可。  
- 在 `settings.py` 中添加以下：
```python
DOWNLOADER_MIDDLEWARES = {
    ...
    'yourproject.middlewares.yourmiddleware': 543,
    # example
    # 'yourproject.middlewares.ManageProxy': 543,
}
# 重试次数设置 （默认为2）
RETRY_TIMES = 2
# 代理池相关 URL 配置
GET_CSRF = 'http://127.0.0.1:8000/ip_proxy/get_csrf/'
GET_PROXY = 'http://127.0.0.1:8000/ip_proxy/get/'
DEL_PROXY = 'http://127.0.0.1:8000/ip_proxy/del/'
```
- 在 `middlewares.py` 中添加以下：
```python
import requests
from datetime import datetime
from twisted.internet.error import TimeoutError
from yourproject.settings import GET_CSRF, GET_PROXY, DEL_PROXY, RETRY_TIMES

session = requests.session()
csrf = session.get(GET_CSRF).json().get('csrf')


def get_proxy():
    return requests.get(GET_PROXY).json()


def del_proxy(ip, port, verify_time):
    return session.post(DEL_PROXY, {'csrfmiddlewaretoken': csrf, 'ip': ip, 'port': port, 'verify_time': verify_time})


class ManageProxy(object):
    def process_request(self, request, spider):
        if request.meta.get('retry_times') or request.meta.get('proxy'):
            pass
        else:
            proxy_json = get_proxy()
            request.meta['proxy'] = proxy_json.get('proxy')
            request.meta['ip_proxy'] = proxy_json.get('ip')
            request.meta['port_proxy'] = proxy_json.get('port')
            request.meta['verify_time'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

    def process_exception(self, request, exception, spider):
        if all([isinstance(exception, TimeoutError),
                request.meta.get('retry_times') == RETRY_TIMES]):
            item = request.meta['item']
            verify_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            del_proxy(item['ip'], item['port'], verify_time)
        # return request.copy()
```
## 拓展
可自行拓展代理源网站，建议使用 `scrapy` 。  
使用 `scrapy` 注意要点：
- 继承 `BaseSpider`
- 使用 `IpProxiesItem`
- 含有 `ip` `port` `anonymit` `net_type` `ip_location` （IP PORT 匿名度 类型 位置）字段（ `verify_time` 验证时间会自行处理）
- 请求参数设置 `callback=self.verify_porxy`, `dont_filter=True`
  
具体写法可以参考[这里](https://github.com/LZC6244/ip_proxy_pool/tree/master/spider/ip_proxies/ip_proxies/spiders)除 `verify` 和 `base` 之外的任意 `spider`
## 代理池 API
| Path | Mmethod | Description | Return | Arguments | 
| :--  | :--: | :-- | :-- | :-- |
| get/ | get | 从代理池随机返回一个代理 | JsonResponse | None |
| update/ | post | 更新代理，不存在则插入，存在则 priority +1 和 更新验证时间 | HttpResponse | ip,port,verify_time,[anonymity,net_type,ip_location] |
| del/ | post | 代理 priority -1，若 -1 之后 priority=0 则从库中移除该代理 | HttpResponse | ip,port,verify_time |
| get_csrf/ | post | 获取 csrf 信息，用于验证，无该信息则访问 api 失败 | JsonResponse | None |
| list/ | post | 分页展示所有的代理 | HttpResponse | page |
| admin/ | get | 后台入口 | HttpResponse | None |  

**后台**已创建管理员账户 `admin`  
更改密码可以在本项目的 `ip_proxy_site` 路径下使用以下命令：
```shell script
python manage.py changepassword username(admin)
```
或者创建一个新的管理员：
```shell script
python manage.py createsuperuser
```
## 目前代理源
| 网站名称 | 地址 |
| :-- | :-- |
| 快代理 | [传送门](https://www.kuaidaili.com/free/inha/1/) |
| 免费代理IP库 | [传送门](http://ip.jiangxianli.com/?page=1) |
| 西刺代理 | [传送门](https://www.xicidaili.com/nn/1) |
 
## TODO
- [ ] 增加更多代理源网站
- [ ] 增加定时删除前几天的 `scrapy` `log` 的程序  

see  [TODO_HISTORY](https://github.com/LZC6244/ip_proxy_pool/blob/master/docs/TODO_history.md)
## 建议与改进
[HISTORY](https://github.com/LZC6244/ip_proxy_pool/blob/master/docs/history.md)  
有什么问题或建议或比较好的免费代理网站推荐，欢迎提 [issues](https://github.com/LZC6244/ip_proxy_pool/issues)  
