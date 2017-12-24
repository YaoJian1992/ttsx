from django.shortcuts import render
from django.http import HttpResponse
from utils.wrappers import *
from .models import *
from django.db.models import *
from django.http import JsonResponse
from utils.common import *


@login_permission
def index(request):

    # 查询购物数据
    carts = Carts.objects.filter(cart_user_id=get_session(request, 'userid'))
    carts.total_money = 0
    carts.total_num = 0
    for cart in carts:
        # 单品总价
        cart.single_total = cart.cart_amount * cart.cart_goods.goods_price
        # 累加商品总价
        carts.total_money += cart.single_total
        # 累加商品总数量
        carts.total_num += cart.cart_amount



    return render(request, 'cart/cart.html', locals())


# 购物车添加商品
@login_permission
def add_cart_goods(request):

    # 判断用户是否登录
    if not is_login(request):
        # return redirect('/goods/index/')
        return JsonResponse({'total': -1})

    # 获得商品ID
    goods_id = post(request, 'id')
    # 获得商品数量
    goods_num = post(request, 'num')

    # 如果商品存在，则只更新商品的数量
    try:
        cart = Carts.objects.get(cart_user_id=get_session(request, 'userid'), cart_goods_id=goods_id)
        cart.cart_amount = cart.cart_amount + int(goods_num)
        cart.save()

    # 如果商品不存在，则新增购物车商品记录
    except Carts.DoesNotExist:
        cart = Carts()
        cart.cart_goods_id = goods_id
        cart.cart_user_id = get_session(request, 'userid')
        cart.cart_amount = goods_num
        cart.save()

    # 返回给前端当前用户当前购物车中商品的总数
    total = Carts.objects.filter(cart_user_id=get_session(request, 'userid')).aggregate(Sum('cart_amount'))
    # 聚合函数的结果是一个字典类型{'key', value} cart_amount__sum

    # 返回给前端当前购物车商品数量总和
    return JsonResponse({'total': total['cart_amount__sum']})


# 删除购物车商品
@login_permission
def delete_cart_goods(request):

    # 获得商品ID
    goods_id = post(request, 'goods_id')

    # 是否删除成功
    flag = 1

    try:
        cart = Carts.objects.get(cart_goods_id=goods_id, cart_user_id=get_session(request, 'userid'))
        cart.delete()
    except Carts.DoesNotExist:
        flag = 0

    # 获得当前用户购物车商品总数
    total = Carts.objects.filter(cart_user_id=get_session(request, 'userid')).aggregate(Sum('cart_amount'))

    return JsonResponse({'flag': flag, 'total': total['cart_amount__sum']})


# 编辑商品数量
@login_permission
def edit_cart_goods(request):

    # 获得修改的购物车商品ID
    goods_id = post(request, 'goods_id')
    # 获得修改的购物车商品数量
    goods_num = post(request, 'goods_num')

    try:
        cart = Carts.objects.get(cart_goods_id=goods_id, cart_user_id=get_session(request, 'userid'))
        cart.cart_amount = goods_num
        cart.save()
    except Carts.DoesNotExist:
        pass

    return JsonResponse({'flag': 1})














