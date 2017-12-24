# coding=utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^pay/', views.pay),
    url(r'^pay_success/', views.pay_success),
    url(r'^see_result/', views.see_result),
]
