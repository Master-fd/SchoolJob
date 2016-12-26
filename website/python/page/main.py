#coding:utf8
# __author__ = 'fenton-fd.zhu'

from django.shortcuts import render, render_to_response, HttpResponse
from django.http import HttpRequest
from django.template import loader, RequestContext, Context
from website.python.common.response import ResponsesSingleton
from website.python.userBase.userBase import UserBase
from website.python.organizationInfo.organizationDatabase import OrganizationInfoManager
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
        self.organizationInfoManager = OrganizationInfoManager();

    #获取当前选定学校的所有组织
    def getAllOrganization(self):
        uid = self.request.session.get('universityId', None);  #获取学校id
        #获取所有
        organization = OrganizationInfoManager();
        organizationList = organization.getData(universityId=uid);
        return organizationList;

    #根据搜索条件获取job
    def getJobsByKeyword(self, keyword=None):
        organizationList = self.getAllOrganization();
        jobsList = [];
        for item in organizationList:
            if not keyword:
                #直接在main ajax页面搜索
                name = self.request.GET.get('name', None);
                organizationId = self.request.GET.get('organizationId', None);
                jobsList += self.jobInfoManager.getSearchData(name, organizationId);
            elif keyword=='':
                #直接进来默认获取该学校的所有
                jobsList += self.jobInfoManager.getData(organizationsId=item['id']);
            else:
                #首页搜索进来或者ajax页面搜索
                jobsList += self.jobInfoManager.getSearchData(keyword, None);  #搜索jobname
        newJobsList = [];
        for item in jobsList:
            item['url'] = settings.BASE_URL+'jobInfo/'+item['jobId'];
            newJobsList.append(item);
        return newJobsList;

    def pageMain(self, keyword=None):
        #取出数据库推广的组织
        organizationList = self.getAllOrganization();

        #获取职位
        jobsList = self.getJobsByKeyword(keyword);
        data = {
            'data' : {'popLoginModal' : False,
                      'popAddressModal' : False,
                      'popRegisterModal' : False,
                      'organizationList' : organizationList,
                      'jobsList' : jobsList
                      },
        }
        return render_to_response('main/main.html', context_instance=RequestContext(self.request, data));

    #返回职位详情
    def pageInfo(self, jobId):
        data = self.jobInfoManager.getData(jobId=jobId);
        if data:
            data = data[0];

        return render_to_response('main/jobInfo.html', context_instance=RequestContext(self.request, data));