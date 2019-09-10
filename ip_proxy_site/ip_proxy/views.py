import json
import random
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.middleware.csrf import get_token
from .models import IpProxy


# Create your views here.
def proxy_list(request):
    """
    分页展示所有的代理
    :param request:
    :return:
    """
    p_all = IpProxy.objects.all().order_by('-verify_time')
    # 每页20个代理
    paginator = Paginator(p_all, 20)
    page_num = request.GET.get('page', 1)
    try:
        page_num = int(page_num)
        proxies = paginator.page(page_num)
    except PageNotAnInteger:
        proxies = paginator.page(1)
    except EmptyPage:
        proxies = paginator.page(paginator.num_pages)

    # 进行页码的控制，页面最多显示5个页码
    # 总页数小于5页，页面上显示所有页码
    # 若当前页属于前5页，显示前5页（总页数大于10）
    # 若当前页属于后5页，显示后5页（总页数大于10）
    # 其他情况，显示当前页的前2页，当前页，当前页的后2页
    num_pages = paginator.num_pages
    if num_pages < 5:
        pages_range = range(1, num_pages + 1)
    elif page_num <= 5 and num_pages >= 10:
        pages_range = range(1, 6)
    elif num_pages - page_num < 5:
        pages_range = range(num_pages - 4, num_pages + 1)
    else:
        pages_range = range(max(1, page_num - 2), max(6, page_num + 3))

    return render(request, 'ip_proxy/list.html',
                  {'paginator': paginator, 'proxies': proxies, 'pages_range': pages_range})


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
        'net_type': p.net_type,
        'anonymity': p.anonymity,
        'ip_location': p.ip_location,
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
    verify_time = request.POST.get('verify_time')
    verify_time = datetime.strptime(verify_time, '%Y-%m-%d %H:%M:%S')
    p = IpProxy.objects.filter(ip=ip, port=port)

    # print('*' * 50)
    if p:
        status = 'Update'
        data = p[0]
        data.priority += 1
        data.verify_time = verify_time
        data.save()
    else:
        anonymity = request.POST.get('anonymity')
        net_type = request.POST.get('net_type')
        ip_location = request.POST.get('ip_location')
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
    verify_time = request.POST.get('verify_time')
    verify_time = datetime.strptime(verify_time, '%Y-%m-%d %H:%M:%S')
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
        p.update(priority=priority, verify_time=verify_time)
        return HttpResponse(
            '<p>ip:\t%s</p>\n<p>port:\t%s</p>\n<p>priority(now):\t%s</p><p>The proxy priority has been reduced by '
            'one.</p>' % (
                ip, port, priority))


def get_csrf(request):
    # 从此 URL 获取 csrf 数据
    return JsonResponse(data={'csrf': get_token(request)})
