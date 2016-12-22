#coding:utf8

__author__ = 'fenton-fd.zhu'

from django.conf.urls import url, include
import views



urlpatterns = [
    url('^$', views.home),
    url('^home/$', views.home),   # 首页

    url('^search/$', views.search),   #搜索
    url('^main/(?P<keyword>\w+)/$', views.main),    #社团招聘页
    url('^backgroup/(?P<pageName>\w+)/$', views.studentBackPage),  #后台

]


