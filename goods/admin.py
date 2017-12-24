from django.contrib import admin
from .models import *


@admin.register(GoodsInfo)
class GoodsInfoAdmin(admin.ModelAdmin):

    list_display = ['id', 'goods_name', 'goods_price', 'goods_desc', 'goods_status']
    list_per_page = 10



# admin.site.register(GoodsInfo, GoodsInfoAdmin)