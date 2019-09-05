import json
import random
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from .models import IpProxy


# Create your views here.
def proxy_get(request):
    """
    一个取代理数据的接口
    随机从代理池中取一条数据，返回 json
    :param request:
    :return: json 数据
    """
    p_all = IpProxy.objects.all()
    num = random.randint(0, p_all.count() - 1)
    p = p_all[num]
    proxy = p.net_type.lower() + '://' + p.ip + ':' + p.port
    json_data = {
        'ip': p.ip,
        'port': p.port,
        'anonymity': p.anonymity,
        'net_type': p.net_type,
        'verify_time': p.verify_time,
        'priority': p.priority,
        'proxy': proxy,
    }
    return JsonResponse(data=json_data)


def proxy_update(request):
    """
    更新代理池，该代理存在则 priority 优先级加1
    不存在则将该代理入库，priority 默认为2
    :param request:
    :return:
    """
    ip = request.POST.get('ip')
    port = request.POST.get('port')
    anonymity = request.POST.get('anonymity')
    net_type = request.POST.get('net_type')
    ip_location = request.POST.get('ip_location')
    verify_time = request.POST.get('verify_time')
    if isinstance(verify_time, str):
        verify_time = datetime.strptime(verify_time, '%Y-%m-%d %H:%M:%S')
    p = IpProxy.objects.filter(ip=ip, port=port)

    print('*' * 50)
    if p:
        status = 'Update'
        data = p[0]
        data.priority += 1
        data.save()
    else:
        status = 'Insert'
        IpProxy.objects.create(
            ip=ip,
            port=port,
            anonymity=anonymity,
            net_type=net_type,
            ip_location=ip_location,
            verify_time=verify_time,
        )
    # print('*' * 50)
    # print('successful %s' % p)
    # print(request.body)
    # print('+' * 50)
    return HttpResponse('%s successful!\nip:%s\tport:%s\n%s' % (status, ip, port, request.POST))


def proxy_del(request):
    """
    更新代理池，该代理 priority 优先级减1
    若减1之后 priority=0 则从库中移除该代理
    :param request:
    :return:
    """
    ip = request.POST.get('ip')
    port = request.POST.get('port')
    p = IpProxy.objects.filter(ip=ip, port=port)
    if not p:
        return HttpResponse('<p>ip:\t%s</p>\n<p>port:\t%s</p>\n<p>The proxy does not exist.</p>' % (ip, port))
    priority = p[0].priority
    if priority < 2:
        p.delete()
        return HttpResponse(
            '<p>ip:\t%s</p>\n<p>port:\t%s</p>\n<p>The proxy priority has been deleted.</p>' % (ip, port))
    else:
        priority -= 1
        p.update(priority=priority)
        return HttpResponse(
            '<p>ip:\t%s</p>\n<p>port:\t%s</p>\n<p>priority(now):\t%s</p><p>The proxy priority has been reduced by '
            'one.</p>' % (
                ip, port, priority))


def get_csrf(request):
    # 从此 URL 获取 csrf 数据
    return JsonResponse(data={'csrf': get_token(request)})
