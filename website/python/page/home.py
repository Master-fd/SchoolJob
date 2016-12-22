#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'


from django.shortcuts import render, render_to_response, HttpResponse
from django.http import HttpRequest
from django.template import loader, RequestContext, Context
from website.python.common.response import ResponsesSingleton
from website.python.userBase.userBase import UserBase
from website.python.organizationInfo.organizationDatabase import OrganizationInfoManager

import random
import math
'''
首页
'''
class Home(object):

    def __init__(self, request):
        super(Home, self).__init__();
        self.request = request;

    #获取当前选定学校的所有组织
    def getAllOrganization(self):
        uid = self.request.session.get('universityId', None);  #获取学校id
        #获取所有
        organization = OrganizationInfoManager();
        organizationList = organization.getData(universityId=uid);
        return organizationList;

    #根据输入的组织list，选取一个圆心，围绕圆心生成坐标点,为了html定位，需要按照百分比输出
    #输入的是百分比坐标，center:0--100，radius:0--100
    def pointByCircle(self, center=(50, 50), radius=30, data=[]):
        number = len(data);
        pointList = [];
        centerX = center[0];
        centerY = center[1];
        for i in range(1, number+1):
            item = data[i-1];
            angle = i*360.0/number;
            cx = centerX+radius*math.cos(angle);
            cy = centerY+radius*math.sin(angle);
            x, y, px, py = cx+0.5, cy+0.5, cx, cy;
            if len(item['name']) > 13:  #如果社团名字太长，显示在点的下方
                x, y, px, py = cx-2.5, cy+3, cx, cy;
            point = { #最终需要转成百分比的字符串
                'px' : str(px)+'%',
                'py' : str(py)+'%',
                'x' : str(x)+'%',
                'y' : str(y)+'%',
                'cx' : str(cx)+'%',
                'cy' : str(cy)+'%',
                'id' : 1,
                'name' : item['name'],
                'url' : 'http://127.0.0.1:8000/'+str(item['account'])
            };
            pointList.append(point);
        return pointList;



    def pageHome(self):

        # organizationList = self.getAllOrganization();  #获取所有组织
        organizationList=[]
        for i in range(0, 10):
            item = {'name':'社团联合',
                    'account' : i};
            organizationList.append(item);
        if len(organizationList)<=10:
            pointList = self.pointByCircle((50, 50), 32, organizationList);      #给所有组织增加渲染的坐标
        elif len(organizationList)<=20:
            list1 = organizationList[0:7];
            list2 = organizationList[7:];
            pointList = self.pointByCircle((50, 50), 22, list1);
            pointList += self.pointByCircle((50, 50), 35, list2);
        else:
            list1 = organizationList[0:9];
            list2 = organizationList[9:25];
            list3 = organizationList[25:];
            pointList = self.pointByCircle((50, 50), 22, list1);
            pointList += self.pointByCircle((50, 50), 35, list2);
            pointList += self.pointByCircle((50, 50), 43, list3);
        data = {
            'data' : {'popLoginModal' : False,
                      'popAddressModal' : False,
                      'popRegisterModal' : False,
                      'organizationList':  pointList
                      },
        }
        return render_to_response('home/home.html', context_instance=RequestContext(self.request, data));



