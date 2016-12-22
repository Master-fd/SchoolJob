#coding:utf8

from django.shortcuts import render, render_to_response, HttpResponse
from django.http import HttpRequest
from django.template import loader, RequestContext, Context
from django.core.cache import cache

from website.python.page.home import Home
from website.python.page.main import Main

# Create your views here.



#搜索接口
def search(request):
    dic = {
        'data' : {'popLoginModal' : False,
                  'popAddressModal' : False,
                  'popRegisterModal' : False}
    }

    return render_to_response('home/home.html', context_instance=RequestContext(request, dic));


#首页渲染
def home(request):
    pageHome = Home(request);
    return pageHome.pageHome();

#社团招聘页
def main(request, keyword):
    pageMain = Main(request);
    return pageMain.pageMain(keyword);

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