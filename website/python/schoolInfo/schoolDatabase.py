#coding:utf8
__author__ = 'fenton-fd.zhu'



from website import models
from django.forms import model_to_dict


'''
学校信息
'''
class SchoolInfoManager(object):

    def __init__(self):
        super(SchoolInfoManager, self).__init__();
        self.provinceModel = models.Provinces.objects;
        self.universityModel = models.University.objects;
        self.collegeModel = models.College.objects;

        assert self.provinceModel , 'self.provinceModel=None, Must Not None';
        assert self.universityModel , 'self.universityModel=None, Must Not None';
        assert self.collegeModel , 'self.collegeModel=None, Must Not None';

    #获取所有省份，返回字典，
    def getAllProvinces(self):
        provinces = [];
        try:
            data = self.provinceModel.all();
            for obj in data:
                provinces.append(model_to_dict(obj));
        except Exception as e:
            provinces = [];
        return provinces;

    #根据省份id或者名字获取所有学校, 返回字典
    def getAllUniversityByProvinces(self, provinceId=None):
        schools = [];
        if provinceId:
            try:
                data = self.universityModel.filter(pid=provinceId);
                for obj in data:
                    schools.append(model_to_dict(obj));
            except Exception as e:
                schools = [];
        else:
            try:
                data = self.universityModel.all().first();
                schools.append(model_to_dict(data));
            except Exception as e:
                schools = [];
        return schools;

    #根据学校，获取所有学院
    def getAllCollegeByUniversity(self, universityId=None):
        college = [];
        if universityId:
            try:
                data = self.collegeModel.filter(uid=universityId);
                for obj in data:
                    college.append(model_to_dict(obj));
            except Exception as e:
                college = [];
        else:
            try:
                data = self.collegeModel.all().first();
                college.append(model_to_dict(data));
            except Exception as e:
                college = [];
        return college;


    #根据id获取省份,大学，学院，返回字典，
    def getProvincesUniversityCollegeById(self, provincesId=None, universityId=None, collegeId=None):
        data = {}
        try:
            if provincesId:
                result = self.provinceModel.get(id=provincesId);  #省份
                data['province'] = model_to_dict(result);
            if universityId:
                result = self.universityModel.get(id=universityId);
                data['university'] = model_to_dict(result);
            if collegeId:
                result = self.collegeModel.get(id=collegeId);
                data['college'] = model_to_dict(result);
        except Exception as e:
            data = None;
        return data;