import hashlib
from .wrappers import *
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from users.models import *


# 密码加密
def password_encryption(password):
    # 创建加密对象
    sha = hashlib.sha256()
    # 对明文加密
    new_password = 'helloworld' + password
    sha.update(new_password.encode('utf-8'))
    # 返回密文
    return sha.hexdigest()


# 用户是否登录(装饰器)
def login_permission(view_func):
    def wrapper(request, *args, **kwargs):
        # 检查用户是否登录
        if get_session(request, 'username') and get_session(request, 'userid'):
            # 如果登录则执行视图函数
            return view_func(request, *args, **kwargs)
        else:
            # 如果没有登录,跳转到登录页面
            return redirect(reverse('users:login'))

    return wrapper


# 用户登陆
def is_login(request):
    return get_session(request, 'username') and get_session(request, 'userid')
