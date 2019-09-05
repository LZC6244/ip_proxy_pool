# -*- coding: utf-8 -*-
# @Author: lzc
# @Time  :2019/8/26
from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'ip_proxy'
urlpatterns = [
    path('get/', views.proxy_get, name='get_proxy'),
    path('update/', views.proxy_update, name='update_proxy'),
    path('del/', views.proxy_del, name='del_proxy'),
    path('get_csrf/', views.get_csrf, name='get_csrf'),
]
