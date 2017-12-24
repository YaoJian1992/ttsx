from django.shortcuts import render
from django.http import HttpResponse
from utils.wrappers import *
from cart.models import *
from users.models import *
from django.http import JsonResponse
from .models import *
import time
import random
from django.db import transaction


def index(request):

    # 获得用户选中的订单商品ID列表
    ids = post_list(request, 'goods_ids')
    ids_string = ','.join(ids)
    # 查询用户提交的商品列表
    carts = Carts.objects.filter(cart_user_id=get_session(request, 'userid'), cart_goods_id__in=ids)
    # 计算单品总价、商品总价、商品总数量
    carts.total_num = 0
    carts.total_money = 0
    for cart in carts:
        # 计算单品总价
        cart.single_money = cart.cart_amount * cart.cart_goods.goods_price
        # 累加商品总价
        carts.total_money += cart.single_money
        # 累加商品总数量
        carts.total_num += cart.cart_amount

    # 加上运费总价
    carts.fee = carts.total_money + 10

    # 查询用户信息
    user = User.objects.get(id=get_session(request, 'userid'))

    return render(request, 'orders/place_order.html', locals())


# 处理订单提交
@transaction.atomic
def order_handle(request):

    # 获得支付方式
    pay_style = post(request, 'pay')
    # 订单商品列表
    goods_ids = post(request, 'ids').split(',')

    # 获取购物车提交订单商品列表
    carts = Carts.objects.filter(cart_user_id=get_session(request, 'userid'), cart_goods_id__in=goods_ids)
    user = User.objects.get(id=get_session(request, 'userid'))

    # 创建保存点
    save_point = transaction.savepoint()

    try:
        # 创建订单基本信息
        order_info = OrderInfo()
        order_info.order_addr = user.user_addr
        order_info.order_number = str(user.id) + str(int(time.time())) + str(random.randint(1000, 9999))

        # 计算订单商品总数量和总价格
        total_nums = 0
        total_money = 0
        for cart in carts:
            total_nums += cart.cart_amount
            total_money += cart.cart_amount * cart.cart_goods.goods_price

        order_info.order_money = total_money
        order_info.order_nums = total_nums
        order_info.order_pay = pay_style
        order_info.order_recv = user.user_recv
        order_info.order_tele = user.user_tele
        order_info.order_user = user
        # 保存订单基本信息
        order_info.save()

        # 保存订单所对应的商品
        for cart in carts:
            og = OrderGoods()
            og.og_amount = cart.cart_amount
            og.og_money = cart.cart_amount * cart.cart_goods.goods_price
            og.og_price = cart.cart_goods.goods_price
            og.og_unit = cart.cart_goods.goods_unit
            og.og_order = order_info
            og.save()

        # 删除购物车中的商品信息
        carts.delete()
        # 提交事务
        transaction.savepoint_commit(save_point)
    except:
        # 滚到上一个保存点
        transaction.savepoint_rollback(save_point)
        return JsonResponse({'ret': 0})

    return JsonResponse({'ret': 1})
















