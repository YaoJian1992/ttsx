from django.shortcuts import render
from django.http import HttpResponse
from .functions import *
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from .models import *
from django.http import JsonResponse
from utils.wrappers import *
from itsdangerous  import  TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from orders.models import *
from django.core.paginator import Paginator
from .tasks import *

def index(request):

    return HttpResponse('商品首页!')


# 登陆页面
def login(request):
    return render(request, 'users/login.html', locals())


# 注册页面
def register(request):

    # 从消息框架中读取提示信息
    message = get_info_messages(request)

    return render(request, 'users/register.html', locals())


# 处理注册
def register_handle(request):

    # 如果信息合法，信息入库，跳转到登陆页面
    if check_register_params(request):
        # 数据入库
        User.objects.register_userinfo_save(request)
        # 获得注册信息
        user_name = post(request, 'user_name')
        user_mail = post(request, 'user_mail')
        active_url = create_active_link(request)
        # 发送邮件任务到celery
        send_register_mail.delay(user_name, user_mail, active_url)

        # 跳转到登陆页面
        return redirect(reverse('users:login'))
    else:
        return redirect(reverse('users:register'))
        # 信息不合法，跳转到注册页面


# 检查用户名是否存在
def check_username_exist(request):

    # 获取用户名
    username = get(request, 'username')
    user = User.objects.get_userinfo_by_name(username)
    # 检查用户名是否存在
    if user.username:
        return JsonResponse({'ret': 1})
    else:
        return JsonResponse({'ret': 0})


# 登录处理
def login_handle(request):

    # 对数据进行简单的校验
    if check_login_params(request):
        # 1. 保持用户登录状态(session, 用户名,用户id)
        keep_user_online(request)
        # 2. 记住用户名
        response = redirect(get_url_from_cookie(request))
        remember_username(request, response)
        # 3. 跳转到用户中心
        return response

    else:
        # 返回到登录界面
        return redirect(reverse('users:login'))


# 用户中心
@login_permission
# @add_menu_info
def user_center(request):
    # menus = UserCenterMenu.objects.all()
    # print(locals())
    #local()的数据形式：
    # {'menus': [ < UserCenterMenu: UserCenterMenu
    # object >, < UserCenterMenu: UserCenterMenu
    # object >, < UserCenterMenu: UserCenterMenu
    # object >], 'request': < WSGIRequest: GET
    # '/users/user_center/' >}
    user = User.objects.get_userinfo_by_name(get_session(request,'username'))

    # 用户浏览信息列表
    history_list = GoodsHistory.objects.filter(his_user_id=get_session(request, 'userid')).order_by('-update_time')
    return render(request, 'users/user_center_info.html',locals())

#用户中心-订单
@login_permission
# @add_menu_info
def user_order(request):
    # menus = UserCenterMenu.objects.all()
    user = User.objects.get_userinfo_by_name(get_session(request, 'username'))
    #读取用户订单列表
    orders = OrderInfo.objects.filter(order_user_id=get_session(request,'userid'))
    #创建分页对像
    paginator = Paginator(orders,2)
    #获取当前页码
    page = get(request,'page')
    # 这一部必须有,否则page不是整数而报错
    if not page:
        page = 1
    #获得当前页码数据
    current_data = paginator.page(page)
    return render(request,'users/user_center_order.html',locals())

#用户中心-地址
@login_permission
# @add_menu_info
def user_site(request):
    # menus = UserCenterMenu.objects.all()
    user = User.objects.get_userinfo_by_name(get_session(request, 'username'))
    return  render(request,'users/user_center_site.html',locals())

# 用户登出
def logout(request):
    # 1. 清除用户session
    del_session(request)
    # 2. 跳转到登录页面
    return redirect(reverse('users:login'))

# 更新用户中心—地址页面的信息
def update_address(request):
    # 校验参数
    if check_update_address_params(request):
        #进行前面的简单校验后准备让信息入库
        User.objects.update_user_address(request)

        return redirect(reverse('users:user_site'))

# 用户邮箱激活
def active_handle(request,token):
    serializer = Serializer(settings.SECRET_KEY,3600)
    try:
        #首先说明激活链接没有过期
        #load解密,获得激活链接中的用户id
        user_id = serializer.loads(token).get('id')
        #查询用户
        user = User.objects.get(id = user_id)
        #更新用户激活状态
        user.user_active = True
        user.save()
        return HttpResponse('恭喜您激活成功！')
    except:
        return HttpResponse('激活的链接已经过期!')

# 测试发送邮件
def my_send_mail(request):
    """
           # subject 主题
           # message 邮件文本内容
           # from_email 发送者
           # recipient_list 收件人列表
           # auth_user 邮箱服务器认证用户
           # auth_password 认证密码
           # html_message html邮件内容
           def send_mail(subject, message, from_email, recipient_list,
                     fail_silently=False, auth_user=None, auth_password=None,
                     connection=None, html_message=None):
           """
    # html_content = '<h1>恭喜您，终于注册到了我们的账户!</h1>'
    #
    # send_mail(subject='天天生鲜注册激活测试邮件',
    #           message='', from_email=settings.EMAIL_HOST_USER,
    #           html_message=html_content,
    #           recipient_list=['python199202@163.com'])

    return HttpResponse('发送邮件成功!')







