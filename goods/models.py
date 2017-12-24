from django.db import models
from db.BaseModel import *
from tinymce.models import HTMLField



# 商品分类模型
class GoodsCategory(BaseModel):

    # 商品分类名称
    goods_name = models.CharField(max_length=20)
    # 商品分类样式
    goods_css = models.CharField(max_length=20)
    # 商品分类图片
    goods_image = models.ImageField()


# 商品信息模型
class GoodsInfo(BaseModel):

    # 商品名称
    goods_name = models.CharField(max_length=50)
    # 商品价格
    goods_price = models.DecimalField(max_digits=10, decimal_places=2)
    # 商品概述
    goods_short = models.CharField(max_length=100)
    # 商品描述
    goods_desc = HTMLField()
    # 商品单位
    goods_unit = models.CharField(max_length=30)
    # 商品状态
    goods_status = models.BooleanField(default=True)
    # 商品访问量
    goods_visits = models.IntegerField()
    # 商品销量
    goods_sale = models.IntegerField()
    # 商品图片
    goods_img = models.ImageField()
    # 商品分类
    goods_cag = models.ForeignKey(GoodsCategory)


# 商品图片
class GoodsImages(BaseModel):

    # 图片路径
    img_url = models.CharField(max_length=50)
    # 所属商品
    img_goods = models.ForeignKey(GoodsInfo)


# 首页轮播广告
class ScrollAdvertisement(BaseModel):

    # 广告描述
    ad_name = models.CharField(max_length=30)
    # 广告链接
    ad_link = models.CharField(max_length=100)
    # 广告图片
    ad_image = models.ImageField()
    # 广告顺序
    ad_index = models.SmallIntegerField()


# 活动广告
class ActivityAdvertisement(BaseModel):

    # 活动名称
    ac_name = models.CharField(max_length=30)
    # 活动链接
    ac_link = models.CharField(max_length=100)
    # 活动图片
    ac_image = models.ImageField()
    # 活动顺序
    ac_index = models.SmallIntegerField()
































