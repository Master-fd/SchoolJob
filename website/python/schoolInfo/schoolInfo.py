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

    def __init__(self, request=HttpRequest()):
        super(SchoolRequestManager, self).__init__();
        self.schoolInfoManager = SchoolInfoManager();
        self.request = request;
        assert self.schoolInfoManager, 'self.schoolInfoManager==None, must Not None';
        assert self.request, 'self.request==None, must Not None';

    #管理请求端口,分发任务
    def requestPortManager(self):
        if self.request.method == 'GET':
            operation = self.request.GET.get('operation', None);
            if operation == 'getData':   #获取指定数据
                return self.provincesUniversityCollege();
            elif operation == 'getAllProvinces':
                return self.getAllProvinces();
            elif operation == 'getAllUniversity':
                return self.getAllUniversity();
            elif operation == 'getAllCollege':
                return self.getAllCollege();
            else:
                return ResponsesSingleton.getInstance().responseJsonArray('fail', 'operation有误');
        elif self.request.method == 'POST':
            operation = self.request.POST.get('operation', None);
            if operation == 'set':
                return self.setUniversity();
            else:
                return ResponsesSingleton.getInstance().responseJsonArray('fail', '请使用get或post请求');
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '请使用get或post请求');


    #根据id 获取指定省份
    def provincesUniversityCollege(self):
        provincesId = self.request.POST.get('provincesId', None);
        universityId = self.request.POST.get('universityId', None);
        collegeId = self.request.POST.get('collegeId', None);
        data = self.schoolInfoManager.getProvincesUniversityCollegeById(provincesId, universityId, collegeId);
        if data:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '没有数据');

    #获取所有省份
    def getAllProvinces(self):
        data = self.schoolInfoManager.getAllProvinces();
        if data:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '没有数据');

    #获取该省份所有的学校
    def getAllUniversity(self):
        provinceId = self.request.GET.get('provinceId', None);
        data = self.schoolInfoManager.getAllUniversityByProvinces(provinceId);
        if data:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '没有数据');

    #获取该学校所有学院
    def getAllCollege(self):
        universityId = self.request.GET.get('universityId', None);
        data = self.schoolInfoManager.getAllCollegeByUniversity(universityId);
        if data:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '没有数据');

    #设置指定的学校、省份、院系
    def setUniversity(self):
        provinceId = self.request.POST.get('provinceId', None);
        universityId = self.request.POST.get('universityId', None);
        collegeId = self.request.POST.get('collegeId', None);
        data = self.schoolInfoManager.getProvincesUniversityCollegeById(provinceId, universityId, collegeId);
        if data:
            province = data.get('province', None);
            university = data.get('university', None);
            college = data.get('college', None);
            #设置session
            self.request.session['provinceId'] = province['id'];
            self.request.session['provinceName'] = province['name'];
            self.request.session['universityId'] = university['id'];
            self.request.session['universityName'] = university['name'];
            self.request.session['collegeId'] = college['id'];
            self.request.session['collegeName'] = college['name'];
            data=[province, university, college];
            return ResponsesSingleton.getInstance().responseJsonArray('success', '设置成功', data);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('fail', '设置失败');