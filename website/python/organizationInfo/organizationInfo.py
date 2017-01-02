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
from website.python.userBase.userBase import UserBase
from website.python.schoolInfo.schoolDatabase import SchoolInfoManager
from website.python.studentInfo.studentInfo import ResumeManager
from website.python.jobsInfo.jobsDatabase import JobsInfoManager
from SchoolJob import settings

class OrganizationRequestManager(UserBase):

    def __init__(self, request=HttpRequest()):
        super(OrganizationRequestManager, self).__init__(request);
        self.organizationInfoManager = OrganizationInfoManager();
        self.jobsInfoManager = JobsManager();
        self.jobDbManager = JobsInfoManager();
        self.recvResumInfoManager = RecvResumeManager();
        self.schoolInfoManager = SchoolInfoManager();
        self.resumeManager = ResumeManager();
        self.request = request;

    #管理请求端口,分发任务
    def requestPortManager(self):
        isLogin, account = self.checkIsLogin();   #检查是否login， 获取账号
        if self.request.method == 'POST':
            operation = self.request.POST.get('operation', None);
            if operation == 'register':   #注册
                return self.__userRegister();
            elif operation == 'login':   # 登录
                return self.__userLogin();
            elif operation == 'logout':  #注销
                return self.userLogout();
            elif operation == 'modifyInfo':  #修改基本信息
                return self.__userModify();
            elif operation == 'addUserResume':   #add 简历
                return self.__addRecvResume(account,);
            elif operation == 'modifyResume':   #修改简历
                return self.__modifyRecvResume(account);
            elif operation == 'deleteResume': #删除简历
                return self.__deleteRecvResume(account);
            elif operation == 'addJob':    #增加工作
                return self.__addjob(account);
            elif operation == 'modifyJob':   #修改工作
                return self.__modifyJob(account);
            elif operation == 'deleteJob': #删除工作
                return self.__deleteJob(account);
            else:
                return ResponsesSingleton.getInstance().responseJsonArray('fail', 'operation有误');
        elif self.request.method == 'GET':
            operation = self.request.GET.get('operation', None);
            if operation == 'getUserInfo':   #获取用户资料
                return self.__getUserInfo();
            elif operation == 'isLogin':   #检查是否login
                if isLogin:
                    return ResponsesSingleton.getInstance().responseJsonArray('success', '已登录', [{'isLogin': True,'account': account}]);
                else:
                    return ResponsesSingleton.getInstance().responseJsonArray('fail', '未登录');
            elif operation == 'getResume':   #获取简历
                return self.__getRecvResume(account);
            elif operation == 'getJob':   #获取工作
                return self.__getJob(account);
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
    def __userRegister(self):
        #输入合法性检验
        account = self.request.POST.get('account', None);
        password = self.request.POST.get('password', None);
        name = self.request.POST.get('name', None);
        collegeId = self.request.POST.get('collegeId', None);
        universityId = self.request.POST.get('universityId', None);
        provincesId = self.request.POST.get('provinceId', None);

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
                    'password' : hashPassword,
                    'name' : name,
                    'provincesId' : provincesId,
                    'universityId' : universityId,
                    'collegeId' : collegeId
                };
                result = self.organizationInfoManager.addData(**data);
                if result:
                    data = [{ 'account' : account}];
                    self.request.session['account'] = account;  #注册之后直接登录
                    return ResponsesSingleton.getInstance().responseJsonArray("success", "注册成功", data);
                else:
                    return ResponsesSingleton.getInstance().responseJsonArray("fail", "注册失败，请重试");
        else:
            return ResponsesSingleton.getInstance().responseJsonArray("fail", checkResult);

    #用户登录
    def __userLogin(self):
        #输入合法性检验
        account = self.request.POST.get('account', None);
        password = self.request.POST.get('password', None);
        if account and password:
            #查询数据库
            hash_md5 = hashlib.md5();
            hash_md5.update(password);
            hashPassword = hash_md5.hexdigest();
            try:
                results = self.organizationInfoManager.getData(account=account, password=hashPassword);
                if results:#登录成功
                    user = results[0];
                    universityDict = self.schoolInfoManager.getProvincesUniversityCollegeById(user['provincesId'], user['universityId'], user['collegeId']);
                    province = universityDict.get('province', None);
                    university = universityDict.get('university', None);
                    college = universityDict.get('college', None);
                    self.request.session['account'] = account;
                    self.request.session['provinceId'] = province['id'];
                    self.request.session['provinceName'] = province['name'];
                    self.request.session['universityId'] = university['id'];
                    self.request.session['universityName'] = university['name'];
                    self.request.session['collegeId'] = college['id'];
                    self.request.session['collegeName'] = college['name'];
                    data = [province, university, college];
                    return ResponsesSingleton.getInstance().responseJsonArray("success", "登录成功", data);
                else:
                    return ResponsesSingleton.getInstance().responseJsonArray("fail", "账户或密码错误");
            except Exception, e:
                return ResponsesSingleton.getInstance().responseJsonArray("fail", "账户或密码错误");
        else:
            return ResponsesSingleton.getInstance().responseJsonArray("fail", '账户或密码为空');

    #读取用户基本信息
    def __getUserInfo(self):
        isLogin, account = self.checkIsLogin();
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
    def __userModify(self):
        isLogin, account = self.checkIsLogin();
        if isLogin:
            condition = {};
            if self.request.POST.get('password', None):
                password = self.request.POST.get('password', None);
                hash_md5 = hashlib.md5();
                hash_md5.update(password);
                hashPassword = hash_md5.hexdigest();
                condition['password'] = hashPassword;
            if self.request.POST.get('nickname', None):
                condition['name'] = self.request.POST.get('nickname', None);
            if self.request.POST.get('description', None):
                condition['description'] = self.request.POST.get('description', None);
            print condition, self.request
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
    def __getJob(self, account):
        condition = {
            'jobId' : self.request.GET.get('jobId', None)
        }
        data = self.jobsInfoManager.getData(account, **condition);
        return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);

    #设置job
    def __addjob(self, account):

        data = {
            'name' : self.request.POST.get('name' , None),
            'department' : self.request.POST.get('department', None),
            'description' : self.request.POST.get('description', None),
            'number' : self.request.POST.get('number', None),
        }
        for key, value in data.items():
            if value==None:
                data.pop(key);  #删除值为None的key-value
        results = self.jobsInfoManager.addData(account, **data);
        organizationList = self.organizationInfoManager.getData(account=account);
        organizationInfo = organizationList[0];
        for item in results:
            item['url'] = settings.BASE_URL+'jobInfo/'+item['jobId'];
            item['organization'] = organizationInfo.get('name', None);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '添加成功', results);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');

    #删除job
    def __deleteJob(self, account):

        condition = {
            'jobId' : self.request.POST.get('jobId', None)
        }
        results = self.jobsInfoManager.deleteData(account, **condition);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '删除成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');

    #修改job
    def __modifyJob(self, account):
        jobId = self.request.POST.get('jobId', None),
        data = {
            'name' : self.request.POST.get('name' , None),
            'department' : self.request.POST.get('department', None),
            'description' : self.request.POST.get('description', None),
            'number' : self.request.POST.get('number', None)
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
    def __getRecvResume(self, account):
        condition = {
            'receResumeId' : self.request.GET.get('receResumeId', None)
        }
        data = self.recvResumInfoManager.getData(account, **condition);
        return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);

    #添加RecvResume, 这个account应该是用户
    def __addRecvResume(self, account):

        #根据account获取简历
        resumeList = self.resumeManager.getData(account=account);
        if resumeList:
            resume = resumeList[0];
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '该用户没有简历');
        jobId = self.request.POST.get('jobId', None);
        jobList = self.jobDbManager.getData(jobId=jobId);
        if jobList:
            job = jobList[0];
        organizationList = self.organization.getData(id=job['organizationsId']);
        if organizationList:
            organization = organizationList[0];
        data = {
            'department' : job.get('department', None),
            'jobId' : jobId,
            'resumeId' : resume.get('resumeId', None),
            'name' : resume.get('name', None),
            'sex' : resume.get('sex' , None),
            'college' : resume.get('college' , None),
            'email' : resume.get('email' , None),
            'phoneNumber' : resume.get('phoneNumber' , None),
            'experience' : resume.get('experience' , None),
            'strong' : resume.get('strong' , None),
            'others' : resume.get('others' , None),
            'status' : '新简历',
        }
        for key, value in data.items():
            if value==None:
                data.pop(key);  #删除值为None的key-value

        check = {
            'jobId' : jobId,
            'resumeId' : resume.get('resumeId', None),
        }
        results = self.recvResumInfoManager.getData(organization['account'], **check);
        if not results:
            results = self.recvResumInfoManager.addData(organization['account'], **data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '已发送过了');
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '发送成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '发送失败');

    #删除RecvResume
    def __deleteRecvResume(self, account):

        condition = {
            'receResumeId' : self.request.POST.get('receResumeId', None),
            'jobId' : self.request.POST.get('jobId', None)
        }
        results = self.recvResumInfoManager.deleteData(account, **condition);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '删除成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');

    #修改RecvResume
    def __modifyRecvResume(self, account):
        receResumeId = self.request.POST.get('receResumeId', None),
        data = {
            'status' : self.request.POST.get('status' , None)
        }
        for key, value in data:
            if value==None:
                data.pop(key);  #删除值为None的key-value

        results = self.recvResumInfoManager.modifyData(account, receResumeId, **data);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '修改成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');