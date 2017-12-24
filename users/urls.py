from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^user_center/$', views.user_center, name='user_center'),
    url(r'^user_order/$', views.user_order, name='user_order'),
    url(r'^user_site/$', views.user_site, name='user_site'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_handle/$', views.register_handle, name='register_handle'),
    url(r'^check_username_exist/$', views.check_username_exist, name='check_username_exist'),
    # 处理用户登录
    url(r'^login_handle/$', views.login_handle, name='login_handle'),
    # 用户登出
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^update_address/$', views.update_address, name='update_address'),
    #邮件激活
    url(r'^active_handle/(?P<token>.+/)$', views.active_handle),
    url(r'^my_send_mail/$',views.my_send_mail)

]
