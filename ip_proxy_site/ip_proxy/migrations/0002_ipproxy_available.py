# Generated by Django 2.2.10 on 2020-04-05 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ip_proxy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipproxy',
            name='available',
            field=models.BooleanField(default=None, null=True),
        ),
    ]