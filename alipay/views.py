from django.shortcuts import render
import rsa
import base64
from urllib.parse import quote
from django.http import HttpResponse
from urllib.request import Request, urlopen
import json
from orders.models import *
from utils.wrappers import *

def pay(request):
    order_inofs = OrderInfo.objects.filter(get_session(request, 'userid'))
    for order in order_inofs:
        # order.order_money
        # order.order_nums
        # order.order_fee
        # order.order_number

        # 请求网关
        gateway_url = 'https://openapi.alipaydev.com/gateway.do'

        # 请求参数
        request_params = {
            'app_id': '2016090900470104',
            'method': 'alipay.trade.page.pay',
            'charset': 'utf-8',
            'sign_type': 'RSA2',
            'timestamp': '2014-07-24 03:07:50',
            'return_url': 'http://localhost:8000/alipay/pay_success/',
            'version': '1.0',
            'biz_content': "{'out_trade_no':'order.order_number', "
                           "'product_code':'FAST_INSTANT_TRADE_PAY',"
                           "'subject':'ttsx', "
                           "'total_amount':'order.order_money'}"
        }

        # 对请求参数key按照ascII进行排序
        params_sort = sorted(request_params.items(), key=lambda obj: obj[0])

        # 将参数列表拼接成请求参数字符串
        request_string = ''
        for param in params_sort:
            request_string += '='.join(param) + '&'

        print('request_string:', request_string[:-1])

        # 加载私钥
        with open('/Users/nanmuqingcheng/Desktop/ttsx/private.txt', 'r') as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())

        # 使用私钥对请求参数进行签名
        signature = rsa.sign(request_string[:-1].encode(), private_key, 'SHA-256')

        # 使用base64对签名进行编码
        sign = base64.b64encode(signature).decode()

        # 拼接最后的请求参数
        request_string += 'sign=' + quote(sign)

        # 拼接最终支付URL
        request_string = gateway_url + '?' + request_string

        return render(request, 'pay.html', locals())

#支付成功的跳转页面
def pay_success(request):
    return HttpResponse(' 支付成功！')

# 查询支付结果
def see_result(request):

    # 请求网关
    gateway_url = 'https://openapi.alipaydev.com/gateway.do'
    # 请求参数
    request_params = {
        'app_id': '2016090900470104',
        'method': 'alipay.trade.query',
        'charset': 'utf-8',
        'sign_type': 'RSA2',
        'timestamp': '2014-07-24 03:07:50',
        'version': '1.0',
        'biz_content': "{'out_trade_no':order.order_number}"
    }

    # 对请求参数key按照ascII进行排序
    params_sort = sorted(request_params.items(), key=lambda obj: obj[0])

    # 将参数列表拼接成请求参数字符串
    request_string = ''
    for param in params_sort:
        request_string += '='.join(param) + '&'

    # 加载私钥
    with open('/Users/nanmuqingcheng/Desktop/ttsx/private.txt', 'r') as f:
        private_key = rsa.PrivateKey.load_pkcs1(f.read())

    # 使用私钥对请求参数进行签名
    signature = rsa.sign(request_string[:-1].encode(), private_key, 'SHA-256')

    # 使用base64对签名进行编码
    sign = base64.b64encode(signature).decode()

    # 拼接最后的请求参数
    request_string += 'sign=' + quote(sign)

    # 拼接最终查询支付结果的URL
    request_string = gateway_url + '?' + request_string

    # 封装一个请求对象（退换request_string里面的空格）
    request = Request(request_string.replace(' ', '%20'))

    # 打开链接
    alipay_response = urlopen(request).read().decode()

    # 将json字符串转换为字典对象
    alipay_response_dict = json.loads(alipay_response)

    if alipay_response_dict['alipay_trade_query_response']['code'] == '10000':
        result = '支付宝%s用户支付成功!' % alipay_response_dict['alipay_trade_query_response']['buyer_logon_id']
    else:
        result = '支付失败!'

    return HttpResponse(result)
