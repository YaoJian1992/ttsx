from django.contrib import messages

# get请求
def get(request, key):
    return request.GET.get(key, '').strip()

# post请求
def post(request, key):
    return request.POST.get(key, '').strip()

#post请求，获得是列表的形式
def post_list(request,key):
    return request.POST.getlist(key)

# 封装消息框架
def add_info_message(request, key, value):
    messages.add_message(request, messages.INFO, key + ':' + value)

# 获取提示信息
def get_info_messages(request):

    # 获取提示信息
    mess = messages.get_messages(request)
    # 保存错误信息
    info = dict()

    for message in mess:
        my_info = str(message).split(':')
        info[my_info[0]] = my_info[1]

    return info

# 设置session
def set_session(request, key, value):
    request.session[key] = value


# 获得session
def get_session(request, key):
    return request.session.get(key, '')


# 删除session
def del_session(request):
    request.session.flush()


# 设置cookie
def set_cookie(response, key, value):
    #cookie的有效期24小时
    response.set_cookie(key, value, max_age=60*60*24)


# 删除cookie
def del_cookie(response, key):
    response.delete_cookie(key)


# 获得cookie
def get_cookie(request, key):
    return request.COOKIES.get(key, '')




























