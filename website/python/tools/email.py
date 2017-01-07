#coding:utf8
# __author__ = 'fenton-fd.zhu'

import re
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
from  SchoolJob import settings

'''
发送邮件
'''
class Email(object):

    def __init__(self):
        self.myEmail = settings.DEFAULT_FROM_EMAIL;

    #一次发送一封邮件
    def sendEmail(self, subject, message, toEmail):
        result = False;
        if self.myEmail:
            result = send_mail(subject=subject, message=message, from_email=self.myEmail, recipient_list=toEmail);

        return result;

    #一次性发送多封邮件
    def sendMultiEmail(self, emails=()):
        result = False;
        if self.myEmail:
            temp = [];
            for item in emails:
                item.insert(2, self.myEmail);
                temp.append(item);
            result = send_mass_mail(datatuple=temp, fail_silently=False);

        return result;

    #发送html邮件,经常使用的验证邮件
    def sendAuthEmail(self, subject, html_content, toEmail):

        msg = EmailMultiAlternatives(subject=subject, body=html_content, from_email=self.myEmail, to=toEmail);
        msg.content_subtype = 'html';
        result = msg.send();

        return result

