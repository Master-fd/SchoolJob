#coding:utf8

__author__ = 'fenton-fd.zhu'

from django.conf.urls import url, include
import views



urlpatterns = [
    url('^$', views.home),
    url('^home/$', views.home),   # 首页

    url('^search/$', views.search),
    url('^backgroup/(?P<pageName>\w+)/$', views.studentBackPage),

]


