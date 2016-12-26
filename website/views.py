#coding:utf8

from django.shortcuts import render, render_to_response, HttpResponse
from django.http import HttpRequest
from django.template import loader, RequestContext, Context
from django.core.cache import cache

from website.python.common.response import ResponsesSingleton

from website.python.studentInfo.studentInfo import StudentRequestManager
from website.python.organizationInfo.organizationInfo import OrganizationRequestManager
from website.python.schoolInfo.schoolInfo import SchoolRequestManager

from website.python.studentInfo.studentInfo import StudentInfoManager
from website.python.userBase.userBase import UserBase
from website.python.page.home import Home
from website.python.page.main import Main
from website.python.page.backgroup import Backgroup

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

def resumeInfo(request, resumeId):
    pageBackgroup = Backgroup(request);
    return pageBackgroup.pageResumeInfo(resumeId);

#user后台页面渲染
def userBackPage(request, pageName='home'):
    #获取数据
    pageBackgroup = Backgroup(request);
    return pageBackgroup.pageBackgroup(pageName);

#获取中国学校信息请求
def schoolInfoRequestManager(request):
    schoolRequest = SchoolRequestManager(request);
    return schoolRequest.requestPortManager();

#用户请求
def userInfoRequestPort(request):

    account = request.POST.get('account', None);
    userBase = UserBase(request);
    #先检查已经login或者未login的用户是不是student
    result = userBase.checkUserIsOrganization(account);
    if result:
        #组织
        databaseRequest = OrganizationRequestManager(request);
    else:
        databaseRequest = StudentRequestManager(request);

    response = databaseRequest.requestPortManager();

    return response;

