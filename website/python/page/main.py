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
                #直接在main页面搜索
                name = self.request.GET.get('name', None);
                organizationId = self.request.GET.get('organizationId', None);
                jobsList += self.jobInfoManager.getSearchData(name, organizationId);
            elif keyword=='undefine':
                #直接进来默认获取该学校的所有
                jobsList += self.jobInfoManager.getSearchData(None, item['id'])
            else:
                #首页搜索进来
                jobsList += self.jobInfoManager.getSearchData(keyword, None);  #搜索jobname

        return jobsList;

    def pageMain(self, keyword=None):
        #取出数据库推广的组织
        # organizationList = self.getAllOrganization();
        organizationList = []
        for i in range(0, 5):  #测试数据
            item = {'id' : i, 'name' : '社联','url' : settings.BASE_URL, 'bannerImageUrl' : '/static/image/banner1.jpg'}
            organizationList.append(item);
        #大banner
        bannerList = []
        for item in organizationList:
            item['url'] = settings.BASE_URL+'home/'+str(item['id']);
            bannerList.append(item);
        #搜索,默认是
        # jobsList = self.getJobsByKeyword(keyword);
        jobsList = []
        for i in range(0, 10):
            item = {'name' : '跨级时候好的撒的',
                    'jobId' : i,
                    'url' : settings.BASE_URL,
                    'organizations' : '设立昂',
                    'department' : '高级',
                    'number' : i,
                    'updateDate' : '2011-2-2',
                    'description' : '''工作职责：
                    - 负责从结构/半结构化或无结构的文本中抽取信息，包括但不限于实体、概念及之间的关系
                    - 负责对信息抽取结果合理建模，并高效整理成高质量、高可信的知识
                    - 负责智能产品所需的领域知识库构建以及支撑产品的应用设计与开发
                    职位要求：
                    - 1年及以上大规模数据处理、挖掘、分析等相关工作经验
                    - 熟悉常用数据挖掘、机器学习、自然语言处理工具
                    - 熟悉Linux/Unix开发环境，熟练使用C/C++、Shell/Python语言，具有良好的开发素养'''}
            jobsList.append(item);
        data = {
            'data' : {'popLoginModal' : False,
                      'popAddressModal' : False,
                      'popRegisterModal' : False,
                      'banner' : bannerList,
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