#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'

'''
desc
'''

from django.http import HttpRequest
from django.forms import model_to_dict
import hashlib
import random
from website import models


'''
负责Organization用户基本信息的增删改查
'''
class OrganizationInfoManager(object):

    def __init__(self):
        self.modelObjects = models.OrganizationsInfo.objects;
        assert self.modelObjects , 'self.modelObjects=None, Must Not None';

    #增加基本信息数据
    def addData(self, **kwargs):
        try:
            results = self.modelObjects.create(**kwargs);
            data = [];
            if results:
                data.append(model_to_dict(results));
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
            self.modelObjects.filter(account=account).update(**new);
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
发布的职位信息增删改查, 一对多关系
'''
class JobsManager(object):

    def __init__(self):
        self.organizationModel = models.OrganizationsInfo.objects;
        self.jobsModel = models.Jobs.objects;
        assert self.organizationModel , 'self.organizationModel=None, Must Not None';
        assert self.jobsModel , 'self.jobsModel=None, Must Not None';

    #增加职位信息数据
    def addData(self, account=None, **kwargs):
        try:
            jobId = '00000000';
            while True:
                jobId = str(random.randint(10000000, 100000000))
                if not self.jobsModel.filter(jobId=jobId):
                    break;
            userObj = self.organizationModel.get(account=account);
            kwargs['organizationsId'] = userObj;
            kwargs['jobId'] = jobId;
            results = self.jobsModel.create(**kwargs)
            data = [];
            if results:
                data.append(model_to_dict(results));
        except Exception as e:
            data = None;
        return data;

    #删除一个职位数据
    def deleteData(self, account=None, **kwargs):
        if not account or not kwargs:
            return False
        try:
            userObj = self.organizationModel.get(account=account);
            userObj.jobs_set.filter(**kwargs).delete();
            result = True;
        except Exception as e:
            return False;
        return result;

    #修改职位信息数据
    def modifyData(self, account, jobId, **new):
        try:
            self.jobsModel.filter(account=account, jobId=jobId).update(**new);
            result = True;
        except Exception as e:
            result = False;
        return result;

    #获取该组织的职位数据, 返回数组
    def getData(self, account, **kwargs):
        try:
            userObj = self.organizationModel.get(account=account);
            if kwargs:
                results = userObj.jobs_set.filter(**kwargs);
            else:
                results = userObj.jobs_set.all();
            data = [];
            if results:
                for obj in results:
                    data.append(model_to_dict(obj));
        except Exception as e:
            data = None;
        return data;

    #搜索商品
    def getSearchData(self, account=None, name=None):
        try:
            if not account:
                return None;
            #获取组织
            userObj = self.organizationModel.get(account=account);
            if name:  #获取对应组织的符合条件的职位
                results = userObj.jobs_set.filter(name__icontains=name);
            else:
                results = userObj.jobs_set.all();   #获取所有
            data = [];
            if results:
                for obj in results:
                    item = model_to_dict(obj)
                    item['createDate'] = obj.createDate;
                    item['updateDate'] = obj.updateDate;   #model_to_dict无法转换时间，需要手动转
                    item['organization'] = obj.organizationsId.name;   #社团名
                    item['descriptionLines'] = obj.description.split('\n');   #输出的时候保持字符串分行
                    data.append(item);
        except Exception as e:
            data = None;
        return data;


'''
简历信息增删改查, 一对多关系
'''
class RecvResumeManager(object):

    def __init__(self):
        self.organizationModel = models.OrganizationsInfo.objects;
        self.recvResumeModel = models.ReceResume.objects;
        assert self.organizationModel , 'self.organizationModel=None, Must Not None';
        assert self.recvResumeModel , 'self.recvResumeModel=None, Must Not None';

    #增加接收到的简历信息数据
    def addData(self, account=None, **kwargs):
        try:
            #生成唯一的resumeid
            recvResumeId = '00000000';
            while True:
                recvResumeId = str(random.randint(10000000, 100000000))
                if not self.recvResumeModel.get(recvResumeId=recvResumeId):
                    break;
            userObj = self.organizationModel.get(account=account);
            kwargs['organizationsId'] = userObj;
            kwargs['recvResumeId'] = recvResumeId;
            results = self.recvResumeModel.create(**kwargs)
            data = [];
            if results:
                for obj in results:
                    data.append(model_to_dict(obj));
        except Exception as e:
            data = None;
        return data;

    #删除收到的简历数据
    def deleteData(self, account=None, **kwargs):
        try:
            userObj = self.organizationModel.get(account=account);
            userObj.receresume_set.filter(**kwargs).delete();
            result = True;
        except Exception as e:
            return False;
        return result;

    #修改简历处理信息数据
    def modifyData(self, account, recvResumeId, **new):
        try:
            self.recvResumeModel.filter(account=account, recvResumeId=recvResumeId).update(**new);
            result = True;
        except Exception as e:
            result = False;
        return result;

    #获取简历数据, 返回数组
    def getData(self, account, **kwargs):
        try:
            userObj = self.organizationModel.get(account=account);
            if kwargs:
                results = userObj.receresume_set.filter(**kwargs);
            else:
                results = userObj.receresume_set.all();
            data = [];
            if results:
                for obj in results:
                    data.append(model_to_dict(obj));
        except Exception as e:
            data = None;
        return data;

