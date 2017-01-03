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
import re
# Create your views here.


#页面吧已失效
def noResult(request):
    data = {};
    return render_to_response('common/noresult.html', context_instance=RequestContext(request, data));
#首页渲染
def home(request):
    pageHome = Home(request);
    return pageHome.pageHome();

#社团招聘页
def main(request):
    pageMain = Main(request);
    return pageMain.pageMain();

#job详情
def jobInfo(request, jobId):
    pageMain = Main(request);
    return pageMain.pageInfo(jobId);

#简历详情
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
    isOrganization = userBase.checkUserIsOrganization(account);
    if isOrganization:
        #组织
        databaseRequest = OrganizationRequestManager(request);
    else:
        databaseRequest = StudentRequestManager(request);

    response = databaseRequest.requestPortManager();

    return response;

#resume请求
def resumeInfoRequestPort(request):
    userBase = UserBase(request);
    isLogin, account = userBase.checkIsLogin()
    if isLogin:
        match = re.match('\d+', account);
        if match:
            #添加到组织接收简历
            organizationRequest = OrganizationRequestManager(request);
            #添加到用户已发送简历
            studentRequest = StudentRequestManager(request);
            studentRequest.requestPortManager();
            return organizationRequest.requestPortManager();
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '组织不能发送简历');
    else:
        return ResponsesSingleton.getInstance().responseJsonArray('fail', '您尚未登录');

#用户删除applicant记录
def deleteApplicant(request):
    userBase = UserBase(request);
    isLogin, account = userBase.checkIsLogin()
    if isLogin:
        studentRequest = StudentRequestManager(request);
        return studentRequest.requestPortManager();
    else:
        return ResponsesSingleton.getInstance().responseJsonArray('fail', '您尚未登录');
#搜索业务
def searchInfoRequest(request):
    pageMain = Main(request);
    return pageMain.searchInfoRequest();


