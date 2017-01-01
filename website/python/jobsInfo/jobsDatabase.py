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
                    dict = model_to_dict(obj);
                    dict['createDate'] = obj.createDate;
                    dict['updateDate'] = obj.updateDate;   #model_to_dict无法转换时间，需要手动转
                    dict['organization'] = obj.organizationsId.name;   #社团名
                    dict['descriptionLines'] = obj.description.split('\n');   #输出的时候保持字符串分行
                    data.append(dict);
        except Exception as e:
            data = None;
        return data;
