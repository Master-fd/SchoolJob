#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'


from django.shortcuts import render, render_to_response, HttpResponse
from django.http import HttpRequest
from django.template import loader, RequestContext, Context
from website.python.common.response import ResponsesSingleton

from website.python.studentInfo.studentInfo import ResumeManager
from website.python.organizationInfo.organizationInfo import JobsManager
from website.python.organizationInfo.organizationDatabase import  OrganizationInfoManager
from website.python.userBase.userBase import UserBase
from website.python.studentInfo.studentInfo import StudentInfoManager
from SchoolJob import settings

'''
后台渲染
'''
class Backgroup(object):
    def __init__(self, request=HttpRequest()):
        super(Backgroup, self).__init__();
        self.request = request;
        self.resumeManager = ResumeManager();
        self.jobsManager = JobsManager();
        self.organizationInfoManager = OrganizationInfoManager();



    def pageResumeInfo(self, resumeId):
        if resumeId:
            data = self.resumeManager.getData(resumeId);
            print data;
            if data:
                data = {
                    'data' : data[0]
                }
        else:
            data = {}
        return render_to_response('backgroup/student/resumeInfo.html', context_instance=RequestContext(self.request, data));

    def pageBackgroup(self, pageName):
        page = None;
        data = {};
        #获取数据
        userBase = UserBase(self.request);
        isLogin, account = userBase.checkIsLogin();
        #检测用户类型，student，organization
        if userBase.checkUserIsOrganization():
            #组织
            organizationDb = OrganizationInfoManager();
            results = organizationDb.getData(account=account);
            organizationInfo = results[0];
            if pageName=='me':
                data = {
                        'current' : 'me',
                        'data' : {
                            'name' : organizationInfo.get('name', None),
                            'description' : organizationInfo.get('description', None)
                        }
                    };
                page = 'backgroup/organization/aboutMe.html';
            elif pageName == 'jobs' or pageName == 'home':
                results = self.jobsManager.getData(account=account);
                jobList = [];
                if results:
                    for item in results:   #添加组织名
                        item['organization'] = organizationInfo.get('name', None);
                        item['url'] = settings.BASE_URL+'jobInfo/'+item['jobId'];
                        jobList.append(item);
                data = {
                        'current' : 'jobs',
                        'data' : {
                            'jobsList' : jobList
                        }
                    };
                page = 'backgroup/organization/jobs.html';
            elif pageName == 'resume':
                data = self.resumeManager.getData(account=account);
                if data:
                    data = {
                        'data' : data[0],
                        'current' : 'resume'};
                else:
                    data = {
                        'data' : {},
                        'current' : 'resume'};
                page = 'backgroup/organization/resume.html';
        else:
            #学生
            studentDb = StudentInfoManager();
            results = studentDb.getData(account=account);
            studentInfo = results[0];
            if pageName=='me':
                data = {
                        'current' : 'me',
                        'data' : {
                            'name' : studentInfo.get('name', None),
                            'email' : studentInfo.get('email', None)
                        }
                    };
                page = 'backgroup/student/aboutMe.html';
            elif pageName == 'collect':
                data = {
                        'current' : 'collect',
                        'data' : {

                        }
                    };
                page = 'backgroup/student/collect.html';
            elif pageName == 'applicant' or pageName == 'home':
                data = {
                        'current' : 'applicant',
                        'data' : {

                        }
                    };
                page = 'backgroup/student/applicant.html';
            elif pageName == 'resume':
                data = self.resumeManager.getData(account=account);
                if data:
                    data = {
                        'data' : data[0],
                        'current' : 'resume'};
                else:
                    data = {
                        'data' : {},
                        'current' : 'resume'};
                page = 'backgroup/student/resume.html';


        #渲染返回
        return render_to_response(page, context_instance=RequestContext(self.request, data))