#coding:utf8
__author__ = 'fenton-fd.zhu'

from django.http import HttpRequest
from django.forms import model_to_dict
from website import models

'''
job数据库操作，都必须局限在选定的学校里
'''
class JobsInfoManager(object):
    def __init__(self):
        self.jobsModel = models.Jobs.objects;
        assert self.jobsModel , 'self.jobsModel=None, Must Not None';

    #获取基本信息数据, 返回去数组
    def getData(self, **kwargs):
        try:
            results = self.jobsModel.filter(**kwargs);
            data = [];
            if results:
                for obj in results:
                    data.append(model_to_dict(obj));
        except Exception as e:
            data = None;
        return data;
    #搜索商品
    def getSearchData(self, name, organizationId):
        try:
            condition = {};
            if name:
                condition['name__icontains']=name;
            if organizationId:
                condition['organizationId']=organizationId;
            results = self.jobsModel.filter(**condition);
            data = [];
            if results:
                for obj in results:
                    item = model_to_dict(obj)
                    data.append(item);
        except Exception as e:
            data = None;
        return data;
