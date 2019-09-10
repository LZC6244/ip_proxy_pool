from django.contrib import admin

# Register your models here.
from .models import IpProxy


class IpProxyAdmin(admin.ModelAdmin):
    list_display = ['ip', 'port', 'anonymity', 'net_type', 'ip_location', 'verify_time']
    list_filter = ['anonymity', 'net_type']
    search_fields = ['ip']


admin.site.register(IpProxy, IpProxyAdmin)
