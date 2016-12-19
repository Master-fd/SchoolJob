#coding:utf8

from django.shortcuts import render, render_to_response, HttpResponse
from django.http import HttpRequest
from django.template import loader, RequestContext
from django.core.cache import cache
from website.python.common.response import ResponsesSingleton

# Create your views here.


#检测用户是否已经登录
def checkIsLogin(self, request=HttpRequest()):
    account = None;
    try:
        account = request.session.get('account', None);
        if account:
            return True, account;
        else:
            return False, account;
    except:
        return False, account;

def userInfo(request):
    isLogin, account = checkIsLogin(request);
    return {
        'isLogin': '2',
        'account' : '3'
    }
#搜索接口
def search(request):
    dic = {
        'data' : {'name' : 'feidong'}
    }
    temp = loader.get_template('home/home.html');
    return render(request, temp, dic)
    # return render_to_response('home/home.html', dic);
    # return render_to_response('home/home.html', context_instance=RequestContext(request, dic));


#首页渲染
def home(request):
    print request.path.split('/')
    return HttpResponse('ok')

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