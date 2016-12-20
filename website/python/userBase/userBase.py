#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'

from django.http import HttpRequest
from website.python.common.response import ResponsesSingleton
import json
from SchoolJob import settings

'''
用户基本请求
'''
class UserBase(object):


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

    #注销
    def __userLogout(self, request):
        isLogin, account = self.checkIsLogin(request);
        if isLogin:
            del request.session['account'];
        return ResponsesSingleton.getInstance().responseJsonArray("success", "已退出");



def userInfo(request):
    user = UserBase();
    isLogin, account = user.checkIsLogin(request);


    return {
        'isLogin': json.dumps(isLogin),
        'account' : json.dumps(account),
        'resourceUrl' : json.dumps(settings.BASE_URL),  #请求基地址

    }