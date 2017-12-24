from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from utils.wrappers import *
from .functions import *
from django.core.paginator import Paginator


@get_cart_goods_total
def index(request):

    # 查询商品分类
    cags = GoodsCategory.objects.all()
    for cag in cags:
        # 最新添加的四个商品
        cag.new = cag.goodsinfo_set.all().order_by('-id')[:4]
        # 访问量最高的３个商品
        cag.hot = cag.goodsinfo_set.all().order_by('-goods_visits')[:3]

    # 读取首页轮播广告
    scroll = ScrollAdvertisement.objects.all().order_by('ad_index')
    # 读取首页活动广告
    activity = ActivityAdvertisement.objects.all().order_by('ac_index')

    ret = GoodsInfo.objects.all().aggregate(models.Sum('id'))
    print(ret)

    return render(request, 'goods/index.html', locals())


# 商品详细页面
@get_cart_goods_total
def detail(request):

    # 通过商品ID查询商品
    goods = GoodsInfo.objects.get(id=get(request, 'id'))
    # 获得最新两个商品
    goods_new = GoodsInfo.objects.all().order_by('-id')[:2]
    # 记录用户浏览记录
    record_goods_history(request)

    return render(request, 'goods/detail.html', locals())


# 商品列表页面
@get_cart_goods_total
def goods_list(request, cag, page):

    # 读取商品分类
    cags = GoodsCategory.objects.all()[:6]
    # 获得最新两个商品
    goods_new = GoodsInfo.objects.all().order_by('-id')[:2]
    # 根据分类查询商品列表
    goods_set = GoodsInfo.objects.filter(goods_cag_id=cag)
    # 取出当前排序类型
    type = get(request, 'type')
    if type == 'price':
        goods_set = goods_set.order_by('-goods_price')

    if type == 'hot':
        goods_set = goods_set.order_by('-goods_visits')

    # 创建分页器对象
    paginator = Paginator(goods_set, 10)
    # 取出当前页数据
    current_page_data = paginator.page(page)

    return render(request, 'goods/list.html', locals())


# 测试前台使用富文本编辑器
def rich_text(request):
    return render(request, 'goods/rich.html')



























