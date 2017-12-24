from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^rich_text/$', views.rich_text, name='rich_text'),
    # 商品详细页面
    url(r'^detail/$', views.detail, name='detail'),
    # 商品列表页
    url(r'^list/(?P<cag>\d+)/(?P<page>\d+)/$', views.goods_list, name='list'),
]
