"""
Django settings for ttsx project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import djcelery

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#h#a$17*2o!o3v=v37=zk^=#8#oed(@6$9!7-l(23=*1$p99x1'

# SECURITY WARNING: don't run with debug turned on in production!
#线上环境
DEBUG = True
ALLOWED_HOSTS = ['*',]

#测试环境
# DEBUG = True
# ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 安装app
    'users',
    'goods',
    'cart',
    'orders',
    'tinymce',
    'haystack',
    'djcelery',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'users.middleware.RecordLocation',  # 注册自定义中间件
    # 'users.middleware.TestMidlleware01',
    # 'users.middleware.TestMidlleware02',
)

ROOT_URLCONF = 'ttsx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ttsx.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ttsx_three',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'mysql',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'



# 配置静态文件目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 配置上传路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/goods')


# 富文本编辑器配置
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    # 'theme': 'simple',
    'width': 600,
    'height': 400,
    'language': 'zh-CN',
    'theme_advanced_buttons1': 'bold, italic, underline, strikethrough, justifyleft, justifycenter, justifyright, justifyfull, styleselect, bullist, numlist, outdent, indent, undo,redo, link, unlink, image, cleanup, help, code, table, row_before, row_after, delete_row, separator, rowseparator',
    'theme_advanced_buttons2': 'col_before, col_after, delete_col, hr, removeformat, sub, sup, formatselect, fontselect, fontsizeselect, forecolor,charmap,visualaid,spacer,cut,copy,paste'
}


# 配置发送邮件
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = 'itcast888@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'abc1234567890'
# 收件人看到的发件人
EMAIL_FROM = 'admin<itcast888@163.com>'


# 配置全文检索
HAYSTACK_CONNECTIONS = {
    'default': {
        # 使用whoosh引擎
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        # 索引文件路径
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}
# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 配置每页显示多少查询结果
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 3

# 配置celery
djcelery.setup_loader()
BROKER_URL = 'redis://127.0.0.1:6379/2'
CELERY_IMPORTS = ('users.tasks',)

# 配置站点前台和admin静态文件目录
STATIC_ROOT = os.path.join(BASE_DIR, 'all_static')



