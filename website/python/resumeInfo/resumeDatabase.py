#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'

from django.forms import model_to_dict
from website import models

'''
resume数据库操作
'''
class ResumeInfoManager(object):
    def __init__(self):
        self.resumeModel = models.Resume.objects;
        assert self.resumeModel , 'self.resumeModel=None, Must Not None';

    #获取基本信息数据, 返回去数组
    def getData(self, **kwargs):
        try:
            results = self.resumeModel.filter(**kwargs);
            data = [];
            if results:
                for obj in results:
                    dict = model_to_dict(obj);
                    dict['strongLines'] = obj.strong.split('\n');   #输出的时候保持字符串分行
                    dict['experienceLines'] = obj.experience.split('\n');
                    dict['othersLines'] = obj.others.split('\n');
                    data.append(dict);
        except Exception as e:
            data = None;
        return data;
