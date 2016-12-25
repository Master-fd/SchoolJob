#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'

from django.http import HttpRequest, HttpResponse
from website.python.common.response import ResponsesSingleton
import json
from SchoolJob import settings
from website.python.schoolInfo.schoolDatabase import SchoolInfoManager
from website.python.studentInfo.userDatabase import StudentInfoManager
from website.python.organizationInfo.organizationDatabase import OrganizationInfoManager
import re

'''
用户基本请求
'''
class UserBase(object):


    def __init__(self, request=HttpRequest()):
        super(UserBase, self).__init__();
        self.request = request;
        self.organization = OrganizationInfoManager();
        self.student = StudentInfoManager();
        assert self.request, 'self.request=None, Must Not None';

    #检测用户是否已经登录
    def checkIsLogin(self):
        account = None;
        try:
            account = self.request.session.get('account', None);
            if account:
                return True, account;
            else:
                return False, account;
        except:
            return False, account;

    #检查当前login的用户是否是organization
    def checkUserIsOrganization(self, account):
        if not account:
            isLogin, account = self.checkIsLogin();
        match = re.match('\d+', account);  #不是数字开头就是组织
        if not match:
            return True;
        else:
            return False;


    #注销
    def userLogout(self):
        isLogin, account = self.checkIsLogin();
        if isLogin:
            del self.request.session['account'];
        return ResponsesSingleton.getInstance().responseJsonArray("success", "已退出");

    #获取所有当前选中的学校所有Organization
    def getAllOrganization(self):
        uid = self.request.session.get('universityId', None);  #获取学校id
        #获取所有organization
        organizationList = self.organization.getData(collegeId=uid);
        return organizationList;


#页面渲染固定参数
def userInfo(request=HttpRequest()):
    user = UserBase(request)
    school = SchoolInfoManager();
    isLogin, account = user.checkIsLogin();
    return {
        'isLogin': json.dumps(isLogin),
        'account' : json.dumps(account),
        'university' : request.session.get('universityName', None),  #获取学校名称
        'resourceUrl' : json.dumps(settings.BASE_URL),  #请求基地址
    }