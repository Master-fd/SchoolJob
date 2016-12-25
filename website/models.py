#coding:utf8

from django.db import models

# Create your models here.


#大学,都是一对多关系
#省份
class Provinces(models.Model):
    name = models.CharField(max_length=64, default=None);
#大学，需要关联一个省份
class University(models.Model):
    name = models.CharField(max_length=64, default=None);
    pid = models.CharField(max_length=11);
#学院
class College(models.Model):
    name = models.CharField(max_length=64, default=None);
    uid = models.CharField(max_length=11);

#用户表
class StudentInfo(models.Model):
    account = models.CharField(unique=True, blank=False, max_length=64);
    password = models.CharField(blank=False, max_length=64);
    name = models.CharField(max_length=255, default=None);
    iconUrl = models.CharField(max_length=256);
    email = models.EmailField();
    createDate = models.DateTimeField(auto_now_add=True);
    updateDate = models.DateTimeField(auto_now=True);
    collegeId = models.CharField(max_length=11);#学院
    universityId = models.CharField(max_length=11);
    provincesId = models.CharField(max_length=11);

#学生简历，一对一
class Resume(models.Model):

    resumeId = models.CharField(max_length=64, unique=True);
    account = models.CharField(unique=True, blank=False, max_length=64);
    name = models.CharField(max_length=64);
    sex_choices = (("undefine", u"未定义"),
                   ("male", u"男"),
                ("female", u"女"));
    sex = models.CharField(max_length=64, choices=sex_choices, default=sex_choices[0][0]);
    college = models.CharField(max_length=255);
    email = models.EmailField();
    phoneNumber = models.CharField(max_length=20);
    experience = models.TextField(); #经验
    strong = models.TextField();  #特长
    others = models.TextField();   #其他
    createDate = models.DateTimeField(auto_now_add=True);
    updateDate = models.DateTimeField(auto_now=True);
    studentInfoId = models.OneToOneField('StudentInfo');  #一对一

#学生收藏表
class Collect(models.Model):
    collectId = models.CharField(max_length=64, unique=True);
    jobId = models.CharField(max_length=64);
    name = models.CharField(max_length=64);   #职位名称
    organizations = models.CharField(max_length=255);
    department = models.CharField(max_length=64);
    description = models.TextField();  #职位描述
    status = models.CharField(max_length=10);
    studentInfoId = models.ForeignKey('StudentInfo');

#学生应聘表
class Applicant(models.Model):
    applicantId = models.CharField(max_length=64, unique=True);
    jobId = models.CharField(max_length=64);
    name = models.CharField(max_length=64);   #职位名称
    organizations = models.CharField(max_length=255);
    department = models.CharField(max_length=64);
    applicant = models.TextField();  #职位描述
    status = models.CharField(max_length=10);
    studentInfoId = models.ForeignKey('StudentInfo');

#招聘信息
#社团
class OrganizationsInfo(models.Model):
    account = models.CharField(unique=True, blank=False, max_length=64);
    password = models.CharField(blank=False, max_length=64);
    name = models.CharField(max_length=255, default=None);
    logoUrl = models.CharField(max_length=255); #社团logo
    bannerImageUrl = models.CharField(max_length=255);   #推广图片
    description = models.TextField();  #社团简介描述
    createDate = models.DateTimeField(auto_now_add=True);
    updateDate = models.DateTimeField(auto_now=True);
    collegeId = models.CharField(max_length=11);#学院
    universityId = models.CharField(max_length=11);
    provincesId = models.CharField(max_length=11);

#社团发布的职位信息
class Jobs(models.Model):
    jobId = models.CharField(max_length=64, unique=True);
    name = models.CharField(max_length=64);   #职位名称
    department = models.CharField(max_length=64);
    number = models.CharField(max_length=10, default='0');  #人数
    description = models.TextField();  #职位描述
    createDate = models.DateTimeField(auto_now_add=True);
    updateDate = models.DateTimeField(auto_now=True);
    organizationsId = models.ForeignKey('OrganizationsInfo');  #一对多

#社团收到的简历
class ReceResume(models.Model):
    receResumeId = models.CharField(max_length=64, unique=True);
    department = models.CharField(max_length=255);
    jobId = models.CharField(max_length=64);
    resumeId = models.CharField(max_length=64);
    name = models.CharField(max_length=64);
    sex = models.CharField(max_length=64);
    college = models.CharField(max_length=255);  #学院
    email = models.EmailField();
    phoneNumber = models.CharField(max_length=20);
    experience = models.TextField(); #经验
    strong = models.TextField();  #特长
    others = models.TextField();   #其他
    status = models.CharField(max_length=20);   #status
    createDate = models.DateTimeField(auto_now_add=True);
    updateDate = models.DateTimeField(auto_now=True);
    organizationsId = models.ForeignKey('OrganizationsInfo');  #一对多
