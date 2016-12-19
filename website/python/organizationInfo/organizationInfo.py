#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'

'''
网络请求处理
'''

import hashlib

from django.http import HttpRequest

from website import models
from website.python.common.response import ResponsesSingleton
from organizationDatabase import OrganizationInfoManager, JobsManager, RecvResumeManager


class OrganizationRequestManager(object):

    def __init__(self):
        super(OrganizationRequestManager, self).__init__();
        self.organizationInfoManager = OrganizationInfoManager();
        self.jobsInfoManager = JobsManager();
        self.recvResumInfoManager = RecvResumeManager();

    #管理请求端口,分发任务
    def requestPortManager(self, request=HttpRequest()):
        isLogin, account = self.checkIsLogin(request);   #检查是否login， 获取账号
        if request.method == 'POST':
            operation = request.POST.get('operation', None);
            if operation == 'register':   #注册
                return self.__userRegister(request);
            elif operation == 'login':   # 登录
                return self.__userLogin(request);
            elif operation == 'logout':  #注销
                return self.__userLogout(request);
            elif operation == 'modifyInfo':  #修改基本信息
                return self.__userModify(request);
            elif operation == 'addResume':   #add 简历
                return self.__addRecvResume(account,request);
            elif operation == 'modifyResume':   #修改简历
                return self.__modifyRecvResume(account, request);
            elif operation == 'deleteResume': #删除简历
                return self.__deleteRecvResume(account, request);
            elif operation == 'addJob':    #增加工作
                return self.__addjob(account, request);
            elif operation == 'modifyJob':   #修改工作
                return self.__modifyJob(account, request);
            elif operation == 'deleteJob': #删除工作
                return self.__deleteJob(account, request);
            else:
                return ResponsesSingleton.getInstance().responseJsonArray('fail', 'operation有误');
        elif request.method == 'GET':
            operation = request.GET.get('operation', None);
            if operation == 'getUserInfo':   #获取用户资料
                return self.__getUserInfo(request);
            elif operation == 'isLogin':   #检查是否login
                if isLogin:
                    return ResponsesSingleton.getInstance().responseJsonArray('success', '已登录', [{'isLogin': True,'account': account}]);
                else:
                    return ResponsesSingleton.getInstance().responseJsonArray('fail', '未登录');
            elif operation == 'getResume':   #获取简历
                return self.__getRecvResume(account, request);
            elif operation == 'getJob':   #获取工作
                return self.__getJob(account, request);
            else:
                return ResponsesSingleton.getInstance().responseJsonArray('fail', 'operation有误');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '请使用get或post请求');


#--------------- 基本信息操作--------------------------------------------------------------
    #检测账户密码输入合法性
    def __inputDataCheck(self, account, password, name, provincesId, universityId, collegeId):
        result = True;
        #判断合法性
        if not account:
            result = "账户不能为空";
        if not password:
            result = "密码不能为空";
        if not name:
            result = "组织名不能为空";
        if not provincesId:
            result = "省份不能为空";
        if not universityId:
            result = "大学不能为空";
        if len(account)<6 or len(account)>15:
            result = "合法账户长度6-15位";
        if len(password)<6 or len(password)>15:
            result = "合法密码长度6-15位";
        #检验OK
        return result;

    #用户注册
    def __userRegister(self, request=HttpRequest()):
        #输入合法性检验
        account = request.POST.get('account', None);
        password = request.POST.get('password', None);
        name = request.POST.get('name', None);
        collegeId = request.POST.get('collegeId', None);
        universityId = request.POST.get('universityId', None);
        provincesId = request.POST.get('provincesId', None);

        checkResult = self.__inputDataCheck(account, password, name, provincesId, universityId, collegeId);
        if checkResult == True:
            hash_md5 = hashlib.md5(); #加密
            hash_md5.update(password);
            hashPassword = hash_md5.hexdigest();
            #查询数据库
            result = self.organizationInfoManager.getData(account=account);
            if result:
                return ResponsesSingleton.getInstance().responseJsonArray("fail", "账号已被注册");
            else:
                #插入数据库
                data = {
                    'account' : account,
                    'password' : password,
                    'name' : name,
                    'provincesId' : provincesId,
                    'universityId' : universityId,
                    'collegeId' : collegeId
                };
                result = self.organizationInfoManager.addData(**data);
                if result:
                    data = [{ 'account' : account}];
                    request.session['account'] = account;  #注册之后直接登录
                    return ResponsesSingleton.getInstance().responseJsonArray("success", "注册成功", data);
                else:
                    return ResponsesSingleton.getInstance().responseJsonArray("fail", "注册失败，请重试");
        else:
            return ResponsesSingleton.getInstance().responseJsonArray("fail", checkResult);

    #用户登录
    def __userLogin(self, request=HttpRequest()):
        #输入合法性检验
        account = request.POST.get('account', None);
        password = request.POST.get('password', None);
        if account and password:
            #查询数据库
            hash_md5 = hashlib.md5();
            hash_md5.update(password);
            hashPassword = hash_md5.hexdigest();
            try:
                results = self.organizationInfoManager.getData(account=account, password=hashPassword);
                if results:#登录成功
                    data = [{ 'account' : account}];
                    request.session['account'] = account;
                    return ResponsesSingleton.getInstance().responseJsonArray("success", "登录成功", data);
                else:
                    return ResponsesSingleton.getInstance().responseJsonArray("fail", "账户或密码错误");
            except Exception, e:
                return ResponsesSingleton.getInstance().responseJsonArray("fail", "账户或密码错误");
        else:
            return ResponsesSingleton.getInstance().responseJsonArray("fail", checkResult);

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

    #读取用户基本信息
    def __getUserInfo(self, request=HttpRequest()):
        isLogin, account = self.checkIsLogin(request);
        if isLogin == True:
            #查找用户信息
            data = self.organizationInfoManager.getData(account=account);
            if data:
                return ResponsesSingleton.getInstance().responseJsonArray("success", "查找用户信息", data);
            else:
                return ResponsesSingleton.getInstance().responseJsonArray("fail", "查找失败");
        else:
            return ResponsesSingleton.getInstance().responseJsonArray("fail", "未登录");


    #修改用户基本信息
    def __userModify(self, request=HttpRequest()):
        isLogin, account = self.checkIsLogin(request);
        if isLogin:
            condition = {};
            if request.POST.get('password', None):
                password = request.POST.get('password', None);
                hash_md5 = hashlib.md5();
                hash_md5.update(password);
                hashPassword = hash_md5.hexdigest();
                condition['password'] = hashPassword;
            if request.POST.get('name', None):
                condition['name'] = request.POST.get('name', None);
            if request.POST.get('description', None):
                condition['description'] = request.POST.get('description', None);

            try:
                result = self.organizationInfoManager.modifyData(account, **condition);
                if result:
                    return ResponsesSingleton.getInstance().responseJsonArray('success', '修改成功');
                else:
                    return ResponsesSingleton.getInstance().responseJsonArray('fail', '修改失败');
            except Exception, e:
                return ResponsesSingleton.getInstance().responseJsonArray('fail', '修改失败');
            
#--------------- 发布job信息操作--------------------------------------------------------------

    #读取用户job信息
    def __getJob(self, account, request=HttpRequest()):
        condition = {
            'jobId' : request.GET.get('jobId', None)
        }
        data = self.jobsInfoManager.getData(account, **condition);
        return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);

    #设置job
    def __addjob(self, account, request=HttpRequest()):

        data = {
            'name' : request.POST.get('name' , None),
            'department' : request.POST.get('department', None),
            'description' : request.POST.get('description', None),
            'number' : request.POST.get('number', None),
        }
        for key, value in data:
            if value==None:
                data.pop(key);  #删除值为None的key-value
        results = self.jobsInfoManager.addData(account, **data);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '添加成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');

    #删除job
    def __deleteJob(self, account, request=HttpRequest()):

        condition = {
            'jobId' : request.GET.get('jobId', None)
        }
        results = self.jobsInfoManager.deleteData(account, **condition);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '删除成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');

    #修改job
    def __modifyJob(self, account, request=HttpRequest()):
        jobId = request.POST.get('jobId', None),
        data = {
            'name' : request.POST.get('name' , None),
            'department' : request.POST.get('department', None),
            'description' : request.POST.get('description', None),
            'number' : request.POST.get('number', None)
        }
        for key, value in data:
            if value==None:
                data.pop(key);  #删除值为None的key-value

        results = self.jobsInfoManager.modifyData(account, jobId, **data);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '修改成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');


#--------------- 简历操作--------------------------------------------------------------
    #读取用户接收到的简历信息
    def __getRecvResume(self, account, request=HttpRequest()):
        condition = {
            'receResumeId' : request.GET.get('receResumeId', None)
        }
        data = self.recvResumInfoManager.getData(account, **condition);
        return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);

    #添加RecvResume
    def __addRecvResume(self, account, request=HttpRequest()):

        data = {
            'resumeId' : request.POST.get('resumeId' , None),
            'sex' : request.POST.get('sex' , None),
            'college' : request.POST.get('college' , None),
            'email' : request.POST.get('email' , None),
            'phoneNumber' : request.POST.get('phoneNumber' , None),
            'experience' : request.POST.get('experience' , None),
            'strong' : request.POST.get('strong' , None),
            'others' : request.POST.get('others' , None),
            'status' : request.POST.get('status' , None),
        }
        for key, value in data:
            if value==None:
                data.pop(key);  #删除值为None的key-value
        results = self.recvResumInfoManager.addData(account, **data);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '添加成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');

    #删除RecvResume
    def __deleteRecvResume(self, account, request=HttpRequest()):

        condition = {
            'receResumeId' : request.GET.get('receResumeId', None)
        }
        results = self.recvResumInfoManager.deleteData(account, **condition);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '删除成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');

    #修改RecvResume
    def __modifyRecvResume(self, account, request=HttpRequest()):
        receResumeId = request.POST.get('receResumeId', None),
        data = {
            'status' : request.POST.get('status' , None)
        }
        for key, value in data:
            if value==None:
                data.pop(key);  #删除值为None的key-value

        results = self.recvResumInfoManager.modifyData(account, receResumeId, **data);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '修改成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');