#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'

from website import models
from django.forms import model_to_dict
'''
学校信息
'''


class SchoolInfo(object):

    def __init__(self):
        super(SchoolInfo, self).__init__();
        self.provinceModel = models.Provinces.objects;
        self.university = models.University.objects;
        self.college = models.College.objects;

        assert self.provinceModel , 'self.provinceModel=None, Must Not None';
        assert self.university , 'self.university=None, Must Not None';
        assert self.college , 'self.college=None, Must Not None';

    #获取所有省份，返回字典，
    def provinces(self):
        provinces = [];
        try:
            data = self.provinceModel.all();
            for obj in data:
                provinces.append(model_to_dict(data));
        except Exception as e:
            provinces = [];
        return provinces;

    #根据省份id或者名字获取所有学校, 返回字典
    def universityByProvinces(self, provincesId=None):
        schools = [];
        if provincesId:
            try:
                data = self.university.filter(pid=provincesId);
                for obj in data:
                    schools.append(model_to_dict(obj));
            except Exception as e:
                schools = [];
        return schools;

    #根据学校，获取所有学院
    def collegeByUniversity(self, university=None):
        college = [];
        if university:
            try:
                data = self.college.filter(uid=university);
                for obj in data:
                    college.append(model_to_dict(obj));
            except Exception as e:
                college = [];
        return college;


    #根据id获取省份,大学，学院，返回字典，
    def provincesById(self, provincesId=None, universityId=None, collegeId=None):
        data = {};
        try:
            if provincesId:
                result = self.provinceModel.get(provincesId);  #省份
                data = model_to_dict(result);
            if universityId:
                result = self.university.get(universityId);
                data += model_to_dict(result);
            if collegeId:
                result = self.college.get(collegeId);
                data += model_to_dict(result);
        except Exception as e:
            data = None;
        return data;



