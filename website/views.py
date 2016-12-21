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
                  'popAddressModal' : False,
                  'popRegisterModal' : False}
    }

    return render_to_response('home/home.html', context_instance=RequestContext(request, dic));

#选取一个圆心，围绕圆心生成坐标点
def pointByCircle(center=(), radius=0, number=0):
    pass

#首页渲染
def home(request):
    #围绕一个直径700的圆,需要ajax先发送一个客户端的屏幕的圆心，才可以定点圆心
    organizationList = [
        {'id' : 2,
        'name' : '街舞社',
        'url' : 'http://127.0.0.1:8000/',
         }
    ]
    data = {
        'data' : {'popLoginModal' : False,
                  'popAddressModal' : False,
                  'popRegisterModal' : False,
                  'university': {
                      'organizationList' : organizationList
                  }},
    }
    return render_to_response('home/home.html', context_instance=RequestContext(request, data));

#社团招聘页
def main(request):
    organizationList = [
        {'id' : 2,
        'name' : '街舞社',
        'url' : 'http://127.0.0.1:8000/'}
    ]
    data = {
        'data' : {'popLoginModal' : False,
                  'popAddressModal' : False,
                  'popRegisterModal' : False,
                  'university': {
                      'organizationList' : organizationList
                  }},
    }

    return render_to_response('main/main.html', context_instance=RequestContext(request, data));
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