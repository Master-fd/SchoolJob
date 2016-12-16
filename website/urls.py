#coding:utf8

__author__ = 'fenton-fd.zhu'

from django.conf.urls import url, include
import views



urlpatterns = [
    url('', views.main),
    url('^main/$', views.main),

]


