# coding=utf-8
from django.template import Library
from users.models import *

register = Library()

#自定义过滤器
@register.filter # 激活自定义的过滤器
def get_menu_list(flag):
    # 从数据中读取菜单列表
    menus = UserCenterMenu.objects.all()

    # 创建一个列表用来存放字典
    menu_list = list()

    for menu in menus:
        info = dict()
        info['menu_name'] = menu.menu_name
        info['menu_link'] = menu.menu_link

        if menu.menu_flag == flag:
            info['menu_css'] = 'active'
        else:
            info['menu_css'] = ''

        menu_list.append(info)

    return menu_list

# 时间排序过滤器
@register.filter
def query_set_sort(qs):

    my_list = list()
    for q in qs:
        my_list.append(q)
    my_list.sort(reverse  = True,key=lambda obj: obj.update_time)
    return my_list


