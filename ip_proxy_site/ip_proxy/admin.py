from django.contrib import admin

# Register your models here.
from .models import IpProxy


class IpProxyAdmin(admin.ModelAdmin):
    list_display = ['ip', 'port', 'anonymity', 'net_type', 'ip_location', 'available', 'count', 'verify_time']
    list_filter = ['anonymity', 'net_type', 'available']
    search_fields = ['ip']


admin.site.register(IpProxy, IpProxyAdmin)
