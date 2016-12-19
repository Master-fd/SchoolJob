#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'

from django.http import HttpRequest
from schoolDatabase import SchoolInfoManager
from website.python.common.response import ResponsesSingleton
'''
网络请求数据处理
'''
class SchoolRequestManager(object):

    def __init__(self):
        super(SchoolRequestManager, self).__init__();
        self.schoolInfoManager = SchoolInfoManager();

    #管理请求端口,分发任务
    def requestPortManager(self, request=HttpRequest()):
        if request.method == 'GET':
            operation = request.GET.get('operation', None);
            if operation == 'getData':   #获取指定数据
                return self.provincesUniversityCollege(request);
            elif operation == 'getAllProvinces':
                return self.getAllProvinces(request);
            elif operation == 'getAllUniversity':
                return self.getAllProvinces(request);
            elif operation == 'getAllProvinces':
                return self.getAllProvinces(request);
            else:
                return ResponsesSingleton.getInstance().responseJsonArray('fail', 'operation有误');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '请使用get或post请求');


    #根据id 获取指定省份
    def provincesUniversityCollege(self, request=HttpRequest()):
        provincesId = request.POST.get('provincesId', None);
        universityId = request.POST.get('universityId', None);
        collegeId = request.POST.get('collegeId', None);
        data = self.schoolInfoManager.provincesUniversityCollegeById(provincesId, universityId, collegeId);
        if data:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '没有数据');

    #获取所有省份
    def getAllProvinces(self, request=HttpRequest()):
        data = self.schoolInfoManager.getAllProvinces();
        if data:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '没有数据');

    #获取该省份所有的学校
    def getAllUniversity(self, request=HttpRequest()):
        provincesId = request.GET.get('provincesId', None);
        data = self.schoolInfoManager.getAllUniversityByProvinces(provincesId);
        if data:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '没有数据');

    #获取该学校所有学院
    def getAllCollege(self, request=HttpRequest()):
        universityId = request.GET.get('universityId', None);
        data = self.schoolInfoManager.getAllCollegeByUniversity(universityId);
        if data:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '没有数据');
