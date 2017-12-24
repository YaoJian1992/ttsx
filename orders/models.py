from django.db import models
from db.BaseModel import *
from goods.models import *

#订单基本信息
class OrderInfo(BaseModel):
    status = (
        (1, '待付款'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '以完成'),
    )
    pay = (
        (1, '货到付款'),
        (1, '微信'),
        (1, '支付宝'),
        (1, '银联支付'),
    )
    #订单编号
    order_number = models.CharField(max_length=50)
    #订单状态（与上面的status进行关联）
    order_status = models.SmallIntegerField(choices=status,default=1)
    # 订单收货人
    order_recv = models.CharField(max_length=50)
    # 订单收货地址
    order_addr = models.CharField(max_length=100)
    # 订单收货电话
    order_tele = models.CharField(max_length=11)
    # 订单运费
    order_fee = models.IntegerField(default=10)
    # 订单商品数量
    order_nums = models.IntegerField()
    # 支付方式
    order_pay = models.SmallIntegerField(choices=pay)
    # 订单总金额
    order_money = models.IntegerField()
    # 订单所属用户
    order_user = models.ForeignKey('users.User')


# 订单所属商品列表
class OrderGoods(BaseModel):
    # 商品名称
    og_name = models.CharField(max_length=50)
    # 商品单价
    og_price = models.IntegerField()
    # 商品数量
    og_amount = models.IntegerField()
    # 商品单位
    og_unit = models.CharField(max_length=10)
    # 单品总价
    og_money = models.IntegerField()
    # 所属订单
    og_order = models.ForeignKey(OrderInfo)
    # #商品图片
    # og_img = models.ForeignKey(GoodsInfo)


