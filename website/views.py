#coding:utf8

from django.shortcuts import render, render_to_response, HttpResponse
from django.http import HttpRequest
from django.template import loader, RequestContext, Context
from django.core.cache import cache
from website.python.common.response import ResponsesSingleton

# Create your views here.



#搜索接口
def search(request):
    dic = {
        'data' : {'popLoginModal' : False,
                  'popAddressModal' : True}
    }

    return render_to_response('home/home.html', context_instance=RequestContext(request, dic));


#首页渲染
def home(request):
    data = {
        'data' : {'popLoginModal' : True,
                  'popAddressModal' : False}
    }
    return render_to_response('home/home.html', context_instance=RequestContext(request, data));


#student后台
def studentBackPage(request, pageName='me'):
    #获取数据
    pass
    # if pageName=='me':
    #
    # elif pageName == 'collect':
    #
    # elif pageName == 'applicant':
    #
    # elif pageName == 'resume':

    #渲染返回
    # return ResponsesSingleton.getInstance().returnDrawPage()


#organization后台