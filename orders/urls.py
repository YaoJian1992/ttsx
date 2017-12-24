from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^order_handle/$', views.order_handle, name='order_handle'),
]