# -*- coding: utf-8 -*-
# @Author: lzc
# @Time  : 2019/9/10
import requests

session = requests.session()
csrf = session.get('http://127.0.0.1:8000/ip_proxy/get_csrf/').json().get('csrf')
formdata = {
    'csrfmiddlewaretoken': csrf,
    'ip': '163.204.247.41',
    'port': '12345',
    'net_type': 'HTTP',
    'anonymity': '测试',
    'ip_location': '测试',
    'verify_time': '2019-09-10 11:36:11',
}

session.post('http://127.0.0.1:8000/ip_proxy/update/', formdata)
