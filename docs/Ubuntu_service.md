# 在 Ubuntu 中将本代理池注册成服务。

- 在 `/lib/systemd/system` 新建一个 `IP-proxy-pool.service` 文件，填入下面内容
```shell script
[Unit]
Description= Start IP proxy pool automatically

[Service]
type=forking
WorkingDirectory=/root/ip_proxy_pool
ExecStart=/usr/bin/python scheduler.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
Alias=IP-proxy-pool.service
```
- 启用 `IP-proxy-pool.service` 服务
```shell script
systemctl enable IP-proxy-pool.service
```
- 启动 `IP-proxy-pool.service` 服务
```shell script
systemctl start IP-proxy-pool.service
```
- 查看 `IP-proxy-pool.service` 服务运行状态
```shell script
systemctl status IP-proxy-pool.service
```
显示应类似如下，`Active` 处应为 `active (running)`
```text
● IP-proxy-pool.service - Start IP proxy pool automatically
   Loaded: loaded (/lib/systemd/system/IP-proxy-pool.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2019-09-18 20:05:06 CST; 11min ago
 Main PID: 779 (python)
    Tasks: 9 (limit: 2315)
   CGroup: /system.slice/IP-proxy-pool.service
           ├─ 779 /usr/bin/python scheduler.py
           ├─1239 sh -c python manage.py runserver 0.0.0.0:8000
           ├─1240 python manage.py runserver 0.0.0.0:8000
           └─1479 /usr/bin/python manage.py runserver 0.0.0.0:8000
...
```