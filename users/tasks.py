# coding=utf-8
from celery import task
from django.core.mail import send_mail
from django.conf import settings


# 发送邮件任务
@task
def send_register_mail(user_name, user_mail, active_url):

    html_content = '尊敬的%s，欢迎您注册天天生鲜!<br>请点击链接完成激活:<br>激活地址:%s' % (user_name, active_url)

    send_mail(subject='天天生鲜注册激活邮件',
              message='',
              from_email=settings.EMAIL_HOST_USER,
              html_message=html_content,
              recipient_list=[user_mail])
