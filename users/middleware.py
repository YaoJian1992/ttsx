from utils.wrappers import *
from django.core.urlresolvers import reverse


class RecordLocation(object):

    # 中间件函数不需要全部都写，取决于我们要干预请求相应的阶段
    def process_response(self, request, response):

        valid_urls = [
            reverse('goods:index'),
            reverse('goods:detail'),
        ]

        # localhost:8000/abc/123/?id=19
        # localhost:8000/abc/123/?id=18
        # http://localhost:8000/goods/list/1/5/?type=price
        # /goods/list/1/5/

        if (request.path in valid_urls or request.path.find('/goods/list/') == 0) and response.status_code == 200:
            print('request.path:', request.path)
            # 将用户访问的url写入cookie
            set_cookie(response, 'pre_url', request.get_full_path())

        return response

