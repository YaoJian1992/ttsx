from utils.wrappers import *
import re
from .models import *
from django.contrib import messages
from utils.wrappers import *
from utils.common import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from django.core.mail import send_mail


def check_register_params(request):

    # 获得表单数据
    user_name = post(request, 'user_name')
    user_pass1 = post(request, 'user_pass1')
    user_pass2 = post(request, 'user_pass2')
    user_mail = post(request, 'user_mail')

    flag = True

    if not (5 <= len(user_name) <= 20):
        flag = False
        # 存储错误信息
        # request对象  信息类别messages.INFO 要显示的信息
        # messages.add_message(request, messages.INFO, '您输入的用户名长度不合法!')
        add_info_message(request, 'user_name', '您输入的用户名长度不合法!')

    if not (8 <= len(user_pass1) <= 20):
        flag = False
        # messages.add_message(request, messages.INFO, '您输入的密码长度不合法!')
        add_info_message(request, 'user_pass', '您输入的密码长度不合法!')

    if user_pass1 != user_pass2:
        flag = False
        # messages.add_message(request, messages.INFO, '两次输入密码不一致!')
        add_info_message(request, 'user_pass', '您输入的密码长度不合法!')

    if not re.match('^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', user_mail):
        flag = False
        # messages.add_message(request, messages.INFO, '邮箱格式不合法!')
        add_info_message(request, 'user_mail', '邮箱格式不合法!')

    if User.objects.get_userinfo_by_name(user_name):
        flag = False
        # messages.add_message(request, messages.INFO, '用户名已经存在!')
        add_info_message(request, 'user_name', '用户名已经存在!')

    return flag



# 检测用户登录
def check_login_params(request):

    # 获得登录表单的用户名和密码
    user_name = post(request, 'user_name')
    user_pass = post(request, 'user_pass')

    # 判断用户名和密码的长度是否合法
    if not (5 <= len(user_name) <= 20):
        return False

    if not (8 <= len(user_pass) <= 20):
        return False

    # 查询用户名对应用户信息是否存在
    user = User.objects.get_userinfo_by_name(user_name)
    if not user:
        return False

    # 检查用户输入的密码是否正确
    if user.user_pass != password_encryption(user_pass):
        return False

    return True


# 保持用户登录状态
def keep_user_online(request):

    # 获得用户名
    user_name = post(request, 'user_name')
    # 获得用户id
    user = User.objects.get_userinfo_by_name(user_name)
    user_id = user.id
    # 保存用户名和id
    set_session(request, 'username', user_name)
    set_session(request, 'userid', user_id)


# 记住用户名
def remember_username(request, response):

    # 先取出用户是否点击了记住用户名
    user_remember = post(request, 'user_remember')
    # 判断用户是否点击记住用户名
    if not user_remember:
        return

    # 取出用户名
    user_name = post(request, 'user_name')
    set_cookie(response, 'username', user_name)

# 给request绑定菜单属性
def add_menu_info(view_func):

    def inner(request, *args, **kwargs):
        menus = UserCenterMenu.objects.all()
        # 将菜单列表绑定到request对象上
        request.menus = menus

        return view_func(request, *args, **kwargs)

    return inner

# 用户信息校验
def check_update_address_params(request):

    #获得表单数据
    user_recv = post(request,'user_recv')
    user_addr = post(request,'user_addr')
    user_code = post(request,'user_code')
    user_tele = post(request,'user_tele')

    if len(user_recv) == 0:
        return False
    if len(user_addr) == 0:
        return False
    if len(user_code) != 6:
        return False
    if len(user_tele) != 11:
        return False
    return True

# # 生成激活链接
# def create_active_link(request):
#     serializer = Serializer(settings.SECRET_KEY, 3600)
#     # 查询注册用户的ID
#     user = User.objects.get_userinfo_by_name(post(request, 'user_name'))
#     # 生成激活token
#     token = serializer.dumps({'id': user.id})
#     #通过拼接的方式创建激活链接
#     #token的形式是 b'eyJhbGciOiJIUzI1NiIsImlhdCI6MTUwOTY5O
#     # DY1MSwiZXhwIjoxNTA5Njk4NjYxfQ.eyJpZCI6MTB9.b1O_y-hKn
#     # fgvXTezcPV20HyvB-ITQnNqHpQf99hTHtw'
#     # 是一个非字符串的形式，所以需要decode成字符串
#     url = 'http://localhost:8000/users/active_handle/' + token.decode() + '/'
#     return url

# 生成激活链接
def create_active_link(request):

    serializer = Serializer(settings.SECRET_KEY, 3600)
    # 查询注册用户的ID
    user = User.objects.get_userinfo_by_name(post(request, 'user_name'))
    # 生成激活token
    token = serializer.dumps({'id': user.id})
    # 创建激活链接: http://localhost:8000/users/active_handle/asdasdadas345345/
    url = 'http://localhost:8000/users/active_handle/' + token.decode() + '/'
    return url


# 向用户发送激活邮件
def send_active_mail(request):

    #获得用户注册信息
    user_name = post(request,'user_name')
    user_mail = post(request,'user_mail')

    #生成注册激活链接
    active_url = create_active_link(request)
    # 邮箱注册内容
    html_content = '尊敬的%s，欢迎您注册天天生鲜！<br> 请点击链接完成激活:<br>激活地址：%s' %(user_name,active_url)
    send_mail(subject='天天生鲜注册激活邮件',
              message='', from_email=settings.EMAIL_HOST_USER,
              html_message=html_content,
              recipient_list=[user_mail])


# 从cookie里面获取url
def get_url_from_cookie(request):

    url = get_cookie(request,'pre_url')
    if not url:
        url = reverse('users:user_center')
    return url













