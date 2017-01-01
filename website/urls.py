#coding:utf8

__author__ = 'fenton-fd.zhu'

from django.conf.urls import url, include
import views



urlpatterns = [
    url('^$', views.home),
    url('^home/$', views.home),   # 首页

    url('^main/$', views.main),    #社团招聘页
    url('^jobInfo/(?P<jobId>\d+)/$', views.jobInfo),   #job详情
    url('^resumeInfo/(?P<resumeId>\d+)/$', views.resumeInfo),
    url('^backgroup/(?P<pageName>\w+)/$', views.userBackPage),  #user后台

    #ajax
    url('^schoolInfoRequest/$', views.schoolInfoRequestManager),  #中国学校相关信息请求
    url('^userInfoRequest/$', views.userInfoRequestPort),   #用户请求
    url('^searchInfoRequest/$', views.searchInfoRequest),   # 搜索请求
]


