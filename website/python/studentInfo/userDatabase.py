#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'

'''
user 数据库操作
'''
from django.http import HttpRequest
from django.forms import model_to_dict
import hashlib
import random
from website import models


'''
负责student用户基本信息的增删改查
'''
class StudentInfoManager(object):

    def __init__(self):
        self.modelObjects = models.StudentInfo.objects;
        assert self.modelObjects , 'self.modelObjects=None, Must Not None';

    #增加基本信息数据
    def addData(self, **kwargs):
        try:
            results = self.modelObjects.create(**kwargs);
            data = [];
            if results:
                for obj in results:
                    data.append(model_to_dict(obj));
        except Exception as e:
            data = None;
        return data;

    #删除一个用户
    def deleteData(self, **kwargs):
        try:
            self.modelObjects.filter(**kwargs).delete();
            result = True;
        except Exception as e:
            return False;
        return result;

    #修改基本信息数据
    def modifyData(self, account, **new):
        try:
            self.modelObjects.filter(account).update(**new);
            result = True;
        except Exception as e:
            result = False;
        return result;

    #获取基本信息数据, 返回去数组
    def getData(self, **kwargs):
        try:
            results = self.modelObjects.filter(**kwargs);
            data = [];
            if results:
                for obj in results:
                    data.append(model_to_dict(obj));
        except Exception as e:
            data = None;
        return data;


'''
用户简历信息增删改查，一对一关系
'''
class ResumeManager(object):

    def __init__(self):
        self.studentModel = models.StudentInfo.objects;
        self.resumeModel = models.Resume.objects;
        assert self.studentModel , 'self.studentModel=None, Must Not None';
        assert self.resumeModel , 'self.resumeModel=None, Must Not None';

    #增加简历数据
    def addData(self, account=None, **kwargs):
        try:
            #生成唯一的resumeid
            resumeId = '00000000';
            while True:
                resumeId = str(random.randint(10000000, 100000000))
                if not self.resumeModel.get(resumeId=resumeId):
                    break;

            userObj = self.studentModel.get(account);
            kwargs['studentInfoId'] = userObj;
            kwargs['resumeId'] = resumeId;
            kwargs['account'] = account;
            results = self.resumeModel.create(**kwargs)
            data = [];
            if results:
                for obj in results:
                    data.append(model_to_dict(obj));
        except Exception as e:
            data = None;
        return data;

    #删除一个简历数据
    def deleteData(self, account=None):
        try:
            userObj = self.studentModel.get(account);
            userObj.resume.delete();
            result = True;
        except Exception as e:
            return False;
        return result;

    #修改简历信息数据
    def modifyData(self, account, **new):
        try:
            self.resumeModel.filter(account=account).update(**new);
            result = True;
        except Exception as e:
            result = False;
        return result;

    #获取简历信息数据, 返回数组
    def getData(self, account):
        try:
            userObj = self.studentModel.get(account=account);
            results = userObj.resume;
            data = [];
            if results:
                for obj in results:
                    data.append(model_to_dict(obj));
        except Exception as e:
            data = None;
        return data;


'''
用户收藏信息增删改查, 一对多关系
'''
class ColloctManager(object):

    def __init__(self):
        self.studentModel = models.StudentInfo.objects;
        self.collectModel = models.Collect.objects;
        assert self.studentModel , 'self.studentModel=None, Must Not None';
        assert self.collectModel , 'self.collectModel=None, Must Not None';

    #增加收藏数据
    def addData(self, account=None, **kwargs):
        try:
            collectId = '00000000';
            while True:
                collectId = str(random.randint(10000000, 100000000))
                if not self.collectModel.get(collectId=collectId):
                    break;
            userObj = self.studentModel.get(account);
            kwargs['studentInfoId'] = userObj;
            kwargs['collectId'] = collectId;
            results = self.collectModel.create(**kwargs)
            data = [];
            if results:
                for obj in results:
                    data.append(model_to_dict(obj));
        except Exception as e:
            data = None;
        return data;

    #删除一个收藏数据
    def deleteData(self, account=None, **kwargs):
        try:
            userObj = self.studentModel.get(account);
            userObj.collect_set.filter(**kwargs).delete();
            result = True;
        except Exception as e:
            return False;
        return result;

    #获取搜藏数据, 返回数组
    def getData(self, account, **kwargs):
        try:
            userObj = self.studentModel.get(account=account);
            if kwargs:
                results = userObj.collect_set.filter(**kwargs);
            else:
                results = userObj.collect_set.all();
            data = [];
            if results:
                for obj in results:
                    data.append(model_to_dict(obj));
        except Exception as e:
            data = None;
        return data;

'''
用户应聘信息增删改查, 一对多关系
'''
class ApplicantManager(object):

    def __init__(self):
        self.studentModel = models.StudentInfo.objects;
        self.applicantModel = models.Applicant.objects;
        assert self.studentModel , 'self.studentModel=None, Must Not None';
        assert self.applicantModel , 'self.applicantModel=None, Must Not None';

    #增加应聘数据
    def addData(self, account=None, **kwargs):
        try:
            applicantId = '00000000';
            while True:
                applicantId = str(random.randint(10000000, 100000000))
                if not self.applicantModel.get(applicantId=applicantId):
                    break;
            userObj = self.studentModel.get(account);
            kwargs['studentInfoId'] = userObj;
            kwargs['applicantId'] = applicantId;
            results = self.applicantModel.create(**kwargs)
            data = [];
            if results:
                for obj in results:
                    data.append(model_to_dict(obj));
        except Exception as e:
            data = None;
        return data;

    #删除一个应聘数据
    def deleteData(self, account=None, **kwargs):
        try:
            userObj = self.studentModel.get(account);
            userObj.applicant_set.filter(**kwargs).delete();
            result = True;
        except Exception as e:
            return False;
        return result;

    #获取应聘数据, 返回数组
    def getData(self, account, **kwargs):
        try:
            userObj = self.studentModel.get(account=account);
            results = userObj.applicant_set.filter(**kwargs);
            data = [];
            if results:
                for obj in results:
                    data.append(model_to_dict(obj));
        except Exception as e:
            data = None;
        return data;



