#coding:utf8

__author__ = 'fenton-fd.zhu'

from django.conf.urls import url, include
import views



urlpatterns = [
    url('^$', views.home),
    url('^home/$', views.home),   # 首页

    url('^main/$', views.main),    #社团招聘页
    url('^jobInfo/(?P<jobId>\d+)/$', views.jobInfo),   #job详情
    url('^resumeInfo/(?P<resumeId>\d+)/$', views.resumeInfo),  #简历详情
    url('^backgroup/(?P<pageName>\w+)/$', views.userBackPage),  #user后台
    url('^noresult/$', views.noResult),   #页面已失效

    #ajax
    url('^schoolInfoRequest/$', views.schoolInfoRequestManager),  #中国学校相关信息请求
    url('^userInfoRequest/$', views.userInfoRequestPort),   #用户请求
    url('^resumeInfoRequest/$', views.resumeInfoRequestPort),   #resume请求,发送resume， 组织删除resume
    url('^userDeleteApplicant/$', views.deleteApplicant),   #用户删除applicant记录
    url('^searchInfoRequest/$', views.searchInfoRequest),   # 搜索请求
]


