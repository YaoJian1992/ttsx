from django.db import models
from db.BaseModel import *
from utils.common import *
from utils.wrappers import *


# 用户管理器类
class UserManager(models.Manager):

    # 根据用户名来查询用户
    def get_userinfo_by_name(self, username):

        try:
            return self.get(user_name=username)
        except User.DoesNotExist:
            return None

    # 注册信息入库
    def register_userinfo_save(self, request):

        # 获取表单数据
        user_name = post(request, 'user_name')
        user_pass = post(request, 'user_pass1')
        user_mail = post(request, 'user_mail')

        user = User()
        user.user_name = user_name
        user.user_pass = password_encryption(user_pass)
        user.user_mail = user_mail
        # 保存数据
        user.save()

    # 用户信息入库
    def update_user_address(self, request):
        # 获得用户对象
        user = self.get_userinfo_by_name(get_session(request, 'username'))

        # 如果有用户跳过之前的校验，在这里注册但是没有此用户信息就返回，不将表单的信息入库
        if not user:
            return
        # 数据正式入库
        user.user_recv = post(request, 'user_recv')
        user.user_addr = post(request, 'user_addr')
        user.user_code = post(request, 'user_code')
        user.user_tele = post(request, 'user_tele')
        user.save()

# 用户模型类
class User(BaseModel):

    # 用户名
    user_name = models.CharField(max_length=20, verbose_name='用户名')
    # 用户密码
    user_pass = models.CharField(max_length=64, verbose_name='密码')
    # 邮箱
    user_mail = models.CharField(max_length=30, verbose_name='邮箱')
    # 是否激活
    user_active = models.BooleanField(default=False)
    # 收件人
    user_recv = models.CharField(max_length=10)
    # 收件地址
    user_addr = models.CharField(max_length=50)
    # 电话
    user_tele = models.CharField(max_length=11)
    # 邮编
    user_code = models.CharField(max_length=6)

    # 创建管理器对象
    objects = UserManager()

# 用户中心左侧菜单模型
class UserCenterMenu(BaseModel):
    # 菜单名称
    menu_name = models.CharField(max_length=30)
    # 菜单链接
    menu_link = models.CharField(max_length=100)
    # 菜单标识
    menu_flag = models.CharField(max_length=10)

# 用户浏览商品记录模型
class GoodsHistory(BaseModel):

    #浏览的商品
    his_goods = models.ForeignKey('goods.GoodsInfo')  #通过app名加模型类就可以将his_goods与商品信息GoodsInfo通过外键绑定
    # 浏览的用户
    his_user = models.ForeignKey('User')








