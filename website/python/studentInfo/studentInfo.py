#coding:utf8
__author__ = 'fenton-fd.zhu'

import hashlib

from django.http import HttpRequest

from website import models
from website.python.common.response import ResponsesSingleton
from userDatabase import StudentInfoManager, ResumeManager, ColloctManager, ApplicantManager
from website.python.schoolInfo.schoolDatabase import SchoolInfoManager
from website.python.userBase.userBase import UserBase
from website.python.jobsInfo.jobsDatabase import JobsInfoManager

'''
网络请求数据处理
'''
class StudentRequestManager(UserBase):

    def __init__(self, request=HttpRequest()):
        super(StudentRequestManager, self).__init__(request);
        self.request = request;
        self.studentInfoManager = StudentInfoManager();
        self.resumeInfoManager = ResumeManager();
        self.collectInfoManager = ColloctManager();
        self.applicantInfoManager = ApplicantManager();
        self.schoolInfoManager = SchoolInfoManager();
        self.jobInfoManager = JobsInfoManager();

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
            elif operation == 'modifyInfo':  #修改基本信息'
                return self.__userModify();
            elif operation == 'addResume':   #add 简历
                return self.__addResume(account);
            elif operation == 'modifyResume':   #修改简历
                return self.__modifyResume(account);
            elif operation == 'deleteResume': #删除简历
                return self.__deleteResume(account);
            elif operation == 'addCollect':  #添加收藏
                return self.__addCollect(account);
            elif operation == 'deleteCollect':  #删除收藏
                return self.__deleteCollect(account);
            elif operation == 'addUserResume':  #添加已应聘职位
                return self.__addApplicant(account);
            elif operation == 'deleteApplicant':   #删除已应聘职位
                return self.__deleteApplicant(account);
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
                return self.__getResume(account);
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
    def __userRegister(self):
        #输入合法性检验
        account = self.request.POST.get('account', None);
        password = self.request.POST.get('password', None);
        name = self.request.POST.get('name', None);
        collegeId = self.request.POST.get('collegeId', None);
        universityId = self.request.POST.get('universityId', None);
        provinceId = self.request.POST.get('provinceId', None);

        checkResult = self.__inputDataCheck(account, password, name, provinceId, universityId, collegeId);
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
                    'password' : hashPassword,
                    'name' : name,
                    'provincesId' : provinceId,
                    'universityId' : universityId,
                    'collegeId' : collegeId
                };
                result = self.studentInfoManager.addData(**data);
                if result:
                    user = result[0];
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
                results = self.studentInfoManager.getData(account=account, password=hashPassword);
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
            data = self.studentInfoManager.getData(account=account);
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
            if self.request.POST.get('email', None):
                condition['email'] = self.request.POST.get('email', None);
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
    def __getResume(self, account):
        data = self.resumeInfoManager.getData(account=account);
        return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);

    #设置简历
    def __addResume(self, account):

        data = {
            'name' : self.request.POST.get('name' , None),
            'sex' : self.request.POST.get('sex' , None),
            'college' : self.request.POST.get('college', None),
            'email' : self.request.POST.get('email', None),
            'phoneNumber' : self.request.POST.get('phoneNumber', None),
            'experience' : self.request.POST.get('experience', None),
            'strong' : self.request.POST.get('strong', None),
            'others' : self.request.POST.get('others', None),
        }

        for key, value in data.items():
            if value==None:
                data.pop(key);  #删除值为None的key-value
        results = self.resumeInfoManager.getData(account);
        if results:   #如果已经存在，则修改简历
            results = self.resumeInfoManager.modifyData(account, **data);
        else:
            results = self.resumeInfoManager.addData(account, **data);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '添加成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');


    #删除简历
    def __deleteResume(self, account):
        results = self.resumeInfoManager.deleteData(account);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '删除成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');
    #修改简历
    def __modifyResume(self, account):
        data = {
            'name' : self.request.POST.get('name' , None),
            'sex' : self.request.POST.get('sex' , None),
            'college' : self.request.POST.get('college', None),
            'email' : self.request.POST.get('email', None),
            'phoneNumber' : self.request.POST.get('phoneNumber', None),
            'experience' : self.request.POST.get('experience', None),
            'strong' : self.request.POST.get('strong', None),
            'others' : self.request.POST.get('others', None),
        }

        for key, value in data.items():
            if value==None:
                data.pop(key);  #删除值为None的key-value
        results = self.resumeInfoManager.modifyData(account, **data);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '修改成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '修改失败');

#--------------- 收藏操作--------------------------------------------------------------

    #读取用户collect
    def __getCollect(self, account):
        condition = {
            'collectId' : self.request.GET.get('collectId', None)
        }
        data = self.collectInfoManager.getData(account, **condition);
        return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);

    #设置收藏
    def __addCollect(self, account):
        if not account:
            return ResponsesSingleton.getInstance().responseJsonArray('error', '您尚未登录');
        jobId = self.request.POST.get('jobId' , None);
        #获取指定的job
        jobsList = self.jobInfoManager.getData(jobId=jobId);
        if jobsList:
            job = jobsList[0];
            data = {
                'name' : job['name'],
                'jobId' : jobId,
                'organizations' : job['organization'],
                'department' : job['department'],
                'description' : job['description']
            }
        else:
            data=[];
        results = self.collectInfoManager.getData(account, jobId=jobId);
        if not results:
            results = self.collectInfoManager.addData(account, **data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '已经收藏过了');
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '收藏成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '收藏失败');

    #删除收藏
    def __deleteCollect(self, account):

        condition = {
            'collectId' : self.request.POST.get('collectId', None)
        }
        results = self.collectInfoManager.deleteData(account, **condition);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '删除成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');

#--------------- 应聘操作--------------------------------------------------------------
    #读取用户applicant
    def __getApplicant(self, account):
        condition = {
            'applicantId' : self.request.GET.get('applicantId', None)
        }
        data = self.applicantInfoManager.getData(account, **condition);
        return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);

    #设置applicant
    def __addApplicant(self, account):

        jobId = self.request.POST.get('jobId', None);
        jobList = self.jobInfoManager.getData(jobId=jobId);
        if jobList:
            job = jobList[0];
        organizationList = self.organization.getData(id=job['organizationsId']);
        organization={};
        if organizationList:
            organization = organizationList[0];

        data = {
            'department' : job.get('department', None),
            'jobId' : jobId,
            'name' : job.get('name', None),
            'applicant' : job.get('description', None),
            'organizations' : organization.get('name', None),
            'status' : '已发送'
        }
        check = {
            'jobId' : jobId
        }
        results = self.applicantInfoManager.getData(account, **check);
        if not results:
            results = self.applicantInfoManager.addData(account, **data);
        if results:
            return True;
        else:
            return False;

    #删除applicant
    def __deleteApplicant(self, account):

        condition = {
            'applicantId' : self.request.POST.get('applicantId', None)
        }
        results = self.applicantInfoManager.deleteData(account, **condition);
        if results:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '删除成功');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '删除失败');


