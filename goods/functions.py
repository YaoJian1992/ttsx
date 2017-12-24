# coding=utf-8
from utils.common import *
from users.models import *
from cart.models import *
from django.db.models import *

# 记录用户浏览记录
def record_goods_history(request):

    # 1. 判断用户是否登陆
    if not is_login(request):
        return

    # 2. 用户登陆
    # 2.1 如果商品浏览记录存在,则只更新时间
    # 获得商品ID
    goods_id = get(request, 'id')
    user_id = get_session(request, 'userid')   #  TODO 这里的userid哪里来的
    limit = 5
    try:
        history = GoodsHistory.objects.get(his_goods_id=goods_id, his_user_id=user_id)
        history.save()

    # 2.2 如果商品记录不存在, 新增商品记录
    except GoodsHistory.DoesNotExist:
        # 查询当前用户所有的浏览记录
        history = GoodsHistory.objects.filter(his_user_id=user_id).order_by('update_time')

        # 如果浏览记录条数不够５条, 则直接新增数据
        if history.count() < limit:
            gh = GoodsHistory()
            gh.his_goods_id = goods_id
            gh.his_user_id = user_id
            gh.save()
        # 如果浏览记录条数够５条, 将时间最小的那条记录的商品ID更新为当前商品ID
        else:
            # 这里注意必须用 my_history = history[0]来写不然直接history[0].his_goods_id = goods_id会出现浏览记录不保存的现象
            my_history = history[0]
            my_history.his_goods_id = goods_id
            my_history.save()

#装饰器函数将商品数量绑定在request上，只要将装饰器放在任何有购物车的视图里面都能拿到商品的总数量
#获得购物车商品总数量
def get_cart_goods_total(view_func):

    def inner(request, *args, **kwargs):
        # 商品总数量
        total = 0

        if is_login(request):
            cart = Carts.objects.filter(cart_user_id=get_session(request, 'userid')).aggregate(Sum('cart_amount'))
            #这个是一个表达式（c = a and b or 0）就是如果a是ture表达式的值就是b,如果a的值是false那么表达式的值就是0
            total = cart['cart_amount__sum'] and cart['cart_amount__sum'] or 0

        request.total = total

        return view_func(request,  *args, **kwargs)
    return inner
