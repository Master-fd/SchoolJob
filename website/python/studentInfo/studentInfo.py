#coding:utf8
__author__ = 'fenton-fd.zhu'

from website import models


'''
网络请求数据处理
'''
class StudentRequestManager(models.StudentInfo):
    pass


'''
负责StudentInfo表的增删改查
'''
class StudentInfoManager(models.StudentInfo):

    def __init__(self):
        self.modelObjects = models.StudentInfo.objects;
        assert self.modelObjects , 'self.modelObjects=None, Must Not None';

    #增加数据
    def addData(self, **kwargs):
        try:
            data = self.modelObjects.create(**kwargs);
        except Exception as e:
            data = None;
        return data;

    #删除
    def deleteData(self, **kwargs):
        try:
            self.modelObjects.filter(**kwargs).delete();
            result = True;
        except Exception as e:
            return False;
        return result;

    #修改数据
    def selectData(self, **old, **new):
        try:
            self.modelObjects.filter(**old).update(**new);
            result = True;
        except Exception as e:
            result = False;
        return result;

    #获取数据, 返回去数组
    def getData(self, **kwargs):
        try:
            data = self.modelObjects.filter(**kwargs);
        except Exception as e:
            data = None;
        return data;




