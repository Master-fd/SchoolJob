#coding:utf8
__author__ = 'fenton-fd.zhu'

import hashlib

from django.http import HttpRequest

from website import models
from website.python.common.response import ResponsesSingleton
from userDatabase import StudentInfoManager, ResumeManager, ColloctManager, ApplicantManager

'''
网络请求数据处理
'''
class StudentRequestManager(object):

    def __init__(self):
        super(StudentRequestManager, self).__init__();
        self.studentInfoManager = StudentInfoManager();
        self.resumeInfoManager = ResumeManager();
        self.collectInfoManager = ColloctManager();
        self.applicantInfoManager = ApplicantManager();

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
                return self.__addResume(account,request);
            elif operation == 'modifyResume':   #修改简历
                return self.__modifyResume(account, request);
            elif operation == 'deleteResume': #删除简历
                return self.__deleteResume(account, request);
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
                return self.__getResume(account, request);
            else:
                return ResponsesSingleton.getInstance().responseJsonArray('fail', 'operation有误');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '请使用get或post请求');

#--------------- 基本信息操作--------------------------------------------------------------
    #检测账户密码输入合法性
    def __inputDataCheck(self, account, password, email, provincesId, universityId, collegeId):
        result = True;
        #判断合法性
        if not account:
            result = "账户不能为空";
        if not password:
            result = "密码不能为空";
        if not email:
            result = "Email不能为空";
        if not provincesId:
            result = "省份不能为空";
        if not universityId:
            result = "大学不能为空";
        if not collegeId:
            result = "学院不能为空";
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
        email = request.POST.get('email', None);
        collegeId = request.POST.get('collegeId', None);
        universityId = request.POST.get('universityId', None);
        provincesId = request.POST.get('provincesId', None);

        checkResult = self.__inputDataCheck(account, password, email, provincesId, universityId, collegeId);
        if checkResult == True:
            hash_md5 = hashlib.md5(); #加密
            hash_md5.update(password);
            hashPassword = hash_md5.hexdigest();
            #查询数据库
            result = self.studentInfoManager.getData(account=account);
            if result:
                return ResponsesSingleton.getInstance().responseJsonArray("fail", "账号已被注册");
            else:
                #插入数据库
                data = {
                    'account' : account,
                    'password' : password,
                    'email' : email,
                    'provincesId' : provincesId,
                    'universityId' : universityId,
                    'collegeId' : collegeId
                };
                result = self.studentInfoManager.addData(**data);
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
                results = self.studentInfoManager.getData(account=account, password=hashPassword);
                if results:#登录成功
                    data = [{ 'account' : account}];
                    request.session['account'] = account;
                    return ResponsesSingleton.getInstance().responseJsonArray("success", "登录成功", data);
                else:
                    return ResponsesSingleton.getInstance().responseJsonArray("fail", "账户或密码错误");
            except Exception, e:
                return ResponsesSingleton.getInstance().responseJsonArray("fail", "账户或密码错误");
        else:
            return ResponsesSingleton.getInstance().responseJsonArray("fail", '账户或密码为空');

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
            data = self.studentInfoManager.getData(account=account);
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
            if request.POST.get('nickname', None):
                condition['nickname'] = request.POST.get('nickname', None);
            if request.POST.get('email', None):
                condition['email'] = request.POST.get('email', None);

            try:
                result = self.studentInfoManager.modifyData(account, **condition);
                if result:
                    return ResponsesSingleton.getInstance().responseJsonArray('success', '修改成功');
                else:
                    return ResponsesSingleton.getInstance().responseJsonArray('fail', '修改失败');
            except Exception, e:
                return ResponsesSingleton.getInstance().responseJsonArray('fail', '修改失败');

#--------------- 简历操作--------------------------------------------------------------
    #读取用户简历
    def __getResume(self, account, request=HttpRequest()):
        data = self.resumeInfoManager.getData(account=account);
        return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);

    #设置简历
    def __addResume(self, account, request=HttpRequest()):

        data = {
            'name' : request.POST.get('name' , None),
            'sex' : request.POST.get('sex' , None),
            'college' : request.POST.get('college', None),
            'email' : request.POST.get('email', None),
            'phoneNumber' : request.POST.get('phoneNumber', None),
            'experience' : request.POST.get('experience', None),
            'strong' : request.POST.get('strong', None),
            'others' : request.POST.get('others', None),
        }
        for key, value in data:
            if value==None:
                data.pop(key);  #删除值为None的key-value
        results = self.resumeInfoManager.addData(account, **data);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '添加成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');

    #删除简历
    def __deleteResume(self, account, request=HttpRequest()):
        results = self.resumeInfoManager.deleteData(account);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '删除成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');
    #修改简历
    def __modifyResume(self, account, request=HttpRequest()):
        data = {
            'name' : request.POST.get('name' , None),
            'sex' : request.POST.get('sex' , None),
            'college' : request.POST.get('college', None),
            'email' : request.POST.get('email', None),
            'phoneNumber' : request.POST.get('phoneNumber', None),
            'experience' : request.POST.get('experience', None),
            'strong' : request.POST.get('strong', None),
            'others' : request.POST.get('others', None),
        }

        for key, value in data:
            if value==None:
                data.pop(key);  #删除值为None的key-value

        results = self.resumeInfoManager.modifyData(account, **data);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '修改成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');

#--------------- 收藏操作--------------------------------------------------------------

    #读取用户collect
    def __getCollect(self, account, request=HttpRequest()):
        condition = {
            'collectId' : request.GET.get('collectId', None)
        }
        data = self.collectInfoManager.getData(account, **condition);
        return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);

    #设置收藏
    def __addCollect(self, account, request=HttpRequest()):

        data = {
            'jobId' : request.POST.get('jobId' , None),
            'name' : request.POST.get('name' , None),
            'organizations' : request.POST.get('organizations', None),
            'department' : request.POST.get('department', None),
            'description' : request.POST.get('description', None),
            'status' : request.POST.get('status', None),
        }
        for key, value in data:
            if value==None:
                data.pop(key);  #删除值为None的key-value
        results = self.collectInfoManager.addData(account, **data);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '添加成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');

    #删除收藏
    def __deleteCollect(self, account, request=HttpRequest()):

        condition = {
            'collectId' : request.GET.get('collectId', None)
        }
        results = self.collectInfoManager.deleteData(account, **condition);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '删除成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');

#--------------- 应聘操作--------------------------------------------------------------
    #读取用户applicant
    def __getApplicant(self, account, request=HttpRequest()):
        condition = {
            'applicantId' : request.GET.get('applicantId', None)
        }
        data = self.applicantInfoManager.getData(account, **condition);
        return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);

    #设置applicant
    def __addApplicant(self, account, request=HttpRequest()):

        data = {
            'jobId' : request.POST.get('jobId' , None),
            'name' : request.POST.get('name' , None),
            'organizations' : request.POST.get('organizations', None),
            'department' : request.POST.get('department', None),
            'description' : request.POST.get('description', None),
            'status' : request.POST.get('status', None),
        }
        for key, value in data:
            if value==None:
                data.pop(key);  #删除值为None的key-value
        results = self.applicantInfoManager.addData(account, **data);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '添加成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');

    #删除applicant
    def __deleteApplicant(self, account, request=HttpRequest()):

        condition = {
            'collectId' : request.GET.get('collectId', None)
        }
        results = self.applicantInfoManager.deleteData(account, **condition);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '删除成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');


