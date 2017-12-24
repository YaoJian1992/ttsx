from django.db import models
from db.BaseModel import *

#购物车模型
class Carts(BaseModel):
    #购买的商品
    cart_goods = models.ForeignKey('goods.GoodsInfo')
    #购买的商品数量
    cart_amount = models.IntegerField()
    #所属用户
    cart_user = models.ForeignKey('users.User')
