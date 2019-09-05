# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class IpProxy(models.Model):
    ip = models.CharField(primary_key=True, max_length=20)
    port = models.CharField(max_length=10)
    anonymity = models.CharField(max_length=10)
    net_type = models.CharField(max_length=10)
    ip_location = models.CharField(max_length=100)
    verify_time = models.DateTimeField()
    priority = models.IntegerField(default=2)

    class Meta:
        # managed = False
        db_table = 'ip_proxy'
        unique_together = (('ip', 'port'),)
        ordering = ['-verify_time']

    def __str__(self):
        return self.ip + ':' + self.port
