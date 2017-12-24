# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='是否删除', default=False)),
                ('user_name', models.CharField(verbose_name='用户名', max_length=20)),
                ('user_pass', models.CharField(verbose_name='密码', max_length=64)),
                ('user_mail', models.CharField(verbose_name='邮箱', max_length=30)),
                ('user_active', models.BooleanField(default=False)),
                ('user_recv', models.CharField(max_length=10)),
                ('user_addr', models.CharField(max_length=50)),
                ('user_tele', models.CharField(max_length=11)),
                ('user_code', models.CharField(max_length=6)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserCenterMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='是否删除', default=False)),
                ('menu_name', models.CharField(max_length=30)),
                ('menu_link', models.CharField(max_length=100)),
                ('menu_flag', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
