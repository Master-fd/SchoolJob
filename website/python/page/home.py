#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'

'''
首页处理
'''
from django.shortcuts import render, render_to_response, HttpResponse
from django.http import HttpRequest
from django.template import loader, RequestContext, Context
from website.python.common.response import ResponsesSingleton
from website.python.userBase.userBase import UserBase
from website.python.organizationInfo.organizationDatabase import OrganizationInfoManager

import random
import math

class Home(object):

    def __init__(self, request):
        super(Home, self).__init__();
        self.request = request;
        self.lastangle = 0;


    #选取一个圆心，围绕圆心生成坐标点
    def pointByCircle(self, center=(), radius=600, number=0):

        pointList = []
        centerX = center[0];
        centerY = center[1];
        for i in range(0, number):
            while True:
                angle = random.randint(0, 360);
                if math.fabs(angle-self.lastangle)>10:
                    break;
            if math.fabs(angle-self.lastangle)>10:
                px = centerX+radius*math.cos(angle);
                py = centerY+radius*math.sin(angle);
                if px>=0:
                    x = px-10;
                    y = py+5;
                    cx = px-10;
                    cy = py;
                point = {
                    'px' : px,
                    'py' : py,
                    'x' : x,
                    'y' : y,
                    'cx' : cx,
                    'cy' : cy
                };
                pointList.append(point);
                self.lastangle = angle;

        return pointList;

    def getAllOrganization(self):
        uid = self.request.session.get('universityId', None);  #获取学校id
        #获取所有
        organization = OrganizationInfoManager();
        organizationList = organization.getData(universityId=uid);
        return organizationList;

    def pageHome(self):

        organizationList = self.getAllOrganization();  #获取所有组织
        pointList = self.pointByCircle((100, 100), 100, len(organizationList));      #给所有组织增加渲染的坐标

        newList = []
        for item in organizationList:
            item['url'] = 'http://127.0.0.1:8000/main/keyword'+item['account'];
            item['pointList'] = pointList;
            newList.append(item);
        # organizationList = [
        #     {'id' : 2,
        #     'name' : '街舞社',
        #     'url' : 'http://127.0.0.1:8000/',
        #      'pointList' :
        #      }
        # ]
        data = {
            'data' : {'popLoginModal' : False,
                      'popAddressModal' : False,
                      'popRegisterModal' : False,
                      'organizationList': {
                          'organizationList' : newList
                      }},
        }
        return render_to_response('home/home.html', context_instance=RequestContext(self.request, data));

