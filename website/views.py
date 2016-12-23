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

#job详情
def jobInfo(request, jobId):
    pageMain = Main(request);
    return pageMain.pageInfo(jobId);
#student后台
def studentBackPage(request, pageName='me'):
    #获取数据
    if pageName=='me':
        data = {
        };
        page = 'backgroup/student/aboutMe.html';
    elif pageName == 'collect':
        data = {
        };
        page = 'backgroup/student/collect.html';
    elif pageName == 'applicant':
        data = {
        };
        page = 'backgroup/student/applicant.html';
    elif pageName == 'resume':
        pass
    #渲染返回
    return render_to_response(page, context_instance=RequestContext(request, data))


#organization后台
def organizationBackPage(request, pageName='me'):
    #获取数据
    if pageName=='me':
        data = {
        };
        page = 'backgroup/organization/aboutMe.html';
    elif pageName == 'jobs':
        data = {
        };
        page = 'backgroup/organization/jobs.html';
    elif pageName == 'resume':
        pass
    #渲染返回
    return render_to_response(page, context_instance=RequestContext(request, data))
