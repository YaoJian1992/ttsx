from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    # 购物车添加商品
    url(r'^add_cart_goods', views.add_cart_goods, name='add_cart_goods'),
    # 购物车删除商品
    url(r'^delete_cart_goods', views.delete_cart_goods, name='delete_cart_goods'),
    # 编辑购物车商品数量
    url(r'^edit_cart_goods', views.edit_cart_goods, name='edit_cart_goods'),
]
