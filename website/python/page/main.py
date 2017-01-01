#coding:utf8
# __author__ = 'fenton-fd.zhu'

from django.shortcuts import render, render_to_response, HttpResponse
from django.http import HttpRequest
from django.template import loader, RequestContext, Context
from website.python.common.response import ResponsesSingleton
from website.python.userBase.userBase import UserBase
from website.python.organizationInfo.organizationDatabase import OrganizationInfoManager, JobsManager
from website.python.jobsInfo.jobsDatabase import JobsInfoManager
from SchoolJob import settings

'''
主页
'''
class Main(object):

    def __init__(self, request=HttpRequest()):
        super(Main, self).__init__();
        self.request = request;
        self.jobInfoManager = JobsInfoManager();
        self.jobManager = JobsManager();
        self.organizationInfoManager = OrganizationInfoManager();

    #获取当前选定学校的所有组织
    def getAllOrganization(self):
        uid = self.request.session.get('universityId', None);  #获取学校id
        #获取所有
        organization = OrganizationInfoManager();
        organizationList = organization.getData(universityId=uid);
        return organizationList;

    #根据搜索条件获取job
    def getJobsByKeyword(self):

        organizationAccount = self.request.GET.get('organizationAccount', None);
        jobName = self.request.GET.get('jobName', None);
        jobsList = [];
        if not organizationAccount:
            organizationList = self.getAllOrganization();

            for item in organizationList:
                if not jobName:
                    #遍历改学校的所有组织, 没有jobname，只有组织，则获取所有
                    jobsList += self.jobManager.getSearchData(account=item['account']);
                else:
                    jobsList += self.jobManager.getSearchData(account=item['account'], name=jobName);
        else:
            #有组织，则直接搜索
            jobsList = self.jobManager.getSearchData(account=organizationAccount, name=jobName); #搜索jobname

        newJobsList = [];
        if jobsList:
            for item in jobsList:  #添加url
                item['url'] = settings.BASE_URL+'jobInfo/'+item['jobId'];
                newJobsList.append(item);
        return newJobsList;

    #ajax搜索
    def searchInfoRequest(self):
        #获取职位
        jobsList = self.getJobsByKeyword();
        if jobsList:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '获取成功', jobsList);
        else:
            return ResponsesSingleton.getInstance().responseJsonArray('success', '获取失败', jobsList);

    def pageMain(self):
        #取出数据库d大banner推广的组织
        organizationList = self.getAllOrganization();
        organizationAccount = self.request.GET.get('organizationAccount', None);
        #获取职位
        jobsList = self.getJobsByKeyword();
        data = {
            'data' : {'popLoginModal' : False,
                      'popAddressModal' : False,
                      'popRegisterModal' : False,
                      'organizationList' : organizationList,
                      'jobsList' : jobsList,
                      'currentOrganization' :  organizationAccount
                      },
        }
        return render_to_response('main/main.html', context_instance=RequestContext(self.request, data));

    #返回职位详情
    def pageInfo(self, jobId):
        data = self.jobInfoManager.getData(jobId=jobId);
        if data:
            data = data[0];

        return render_to_response('main/jobInfo.html', context_instance=RequestContext(self.request, data));