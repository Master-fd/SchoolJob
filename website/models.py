#coding:utf8

from django.db import models

# Create your models here.


#大学,都是一对多关系
#省份
class Provinces(models.Model):
    name = models.CharField(max_length=11, default=None);
#大学，需要关联一个省份
class University(models.Model):
    name = models.CharField(max_length=255, default=None),
    pid = models.ForeignKey('Provinces');
#学院
class College(models.Model):
    name = models.CharField(max_length=255, default=None),
    uid = models.ForeignKey('University');

#用户表
class StudentInfo(models.Model):
    account = models.CharField(unique=True, blank=False, max_length=64);
    password = models.CharField(blank=False, max_length=64);
    nickname = models.CharField(max_length=256);
    iconUrl = models.CharField(max_length=256);
    sex_choices = (("undefine", u"未定义"),
                   ("male", u"男"),
                ("female", u"女"));
    sex = models.CharField(max_length=64, choices=sex_choices, default=sex_choices[0][0]);
    collegeid = models.ForeignKey('College');#学院,一对多关联
    email = models.EmailField();
    createDate = models.DateTimeField(auto_now_add=True);
    updateDate = models.DateTimeField(auto_now=True);

#学生简历，一对一
class Resume(models.Model):
    StudentInfo = models.OneToOneField('StudentInfo');  #一对一
    resumeId = models.CharField(max_length=64, unique=True);
    account = models.CharField(unique=True, blank=False, max_length=64);
    name = models.CharField(max_length=64);
    sex_choices = (("undefine", u"未定义"),
                   ("male", u"男"),
                ("female", u"女"));
    sex = models.CharField(max_length=64, choices=sex_choices, default=sex_choices[0][0]);
    collegeid = models.ForeignKey('college');#学院,一对多关联
    email = models.EmailField();
    phoneNumber = models.CharField(max_length=20);
    experience = models.TextField(); #经验
    strong = models.TextField();  #特长
    others = models.TextField();   #其他
    createDate = models.DateTimeField(auto_now_add=True);
    updateDate = models.DateTimeField(auto_now=True);

#招聘信息
#社团等级
class OrganizationsLevel(models.Model):
    level = models.IntegerField(default=0);
    name = models.CharField(max_length=64, default='院级');

#社团
class OrganizationsInfo(models.Model):
    account = models.CharField(unique=True, blank=False, max_length=64);
    password = models.CharField(blank=False, max_length=64);
    name = models.CharField(max_length=255, default=None);
    levelid = models.ForeignKey('OrganizationsLevel'); #一对多
    logoUrl = models.CharField(max_length=255); #社团logo
    description = models.TextField();  #社团简介描述
    universityid = models.ForeignKey('University');#大学,一对多关联
    collegeid = models.ForeignKey('College');#学院,一对多关联

#社团发布的职位信息
class job(models.Model):
    jobId = models.CharField(max_length=64, unique=True);
    name = models.CharField(max_length=64);   #职位名称
    organizationsid = models.ForeignKey('OrganizationsInfo');  #一对多
    department = models.CharField(max_length=64);
    description = models.TextField();  #职位描述
    createDate = models.DateTimeField(auto_now_add=True);
    updateDate = models.DateTimeField(auto_now=True);

