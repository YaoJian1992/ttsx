# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 11:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_goodshistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('og_name', models.CharField(max_length=50)),
                ('og_price', models.IntegerField()),
                ('og_amount', models.IntegerField()),
                ('og_unit', models.CharField(max_length=10)),
                ('og_money', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('order_number', models.CharField(max_length=50)),
                ('order_status', models.SmallIntegerField(choices=[(1, '待付款'), (2, '待发货'), (3, '待收货'), (4, '以完成')], default=1)),
                ('order_recv', models.CharField(max_length=50)),
                ('order_addr', models.CharField(max_length=100)),
                ('order_tele', models.CharField(max_length=11)),
                ('order_fee', models.IntegerField(default=10)),
                ('order_nums', models.IntegerField()),
                ('order_pay', models.SmallIntegerField(choices=[(1, '货到付款'), (1, '微信'), (1, '支付宝'), (1, '银联支付')])),
                ('order_money', models.IntegerField()),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='og_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OrderInfo'),
        ),
    ]