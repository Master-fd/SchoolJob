#coding:utf8
# __author__ = 'fenton-fd.zhu'

import re
from django.http import HttpResponseRedirect
from SchoolJob import settings

class AuthenticationMiddleware(object):

    def process_request(self, request):
        return None

    def process_view(self, request, view, args, kwargs):
        feature = request.path.split('/');
        try:
            if feature[1] == 'backgroup':
                #检测是否login，没有则直接退出
                account = request.session.get('account', None);
                if not account:
                    return HttpResponseRedirect(settings.BASE_URL);
                else:
                    return None;
            else:
                return None;

        except Exception as e:
            return HttpResponseRedirect(settings.BASE_URL);


    def process_exception(self, request, exception):
        return None

    def process_response(self, request, response):
        return response

    def process_template_response(self, request, response):
        """
            传递公共数据
        """
        print 'process_template_response'
        if isinstance(response.context_data, dict):
            response.context_data['isLogin'] = '6'
        else:
            response.context_data = {'account' : '8'}
        return response