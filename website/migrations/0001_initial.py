# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('applicantId', models.CharField(unique=True, max_length=64)),
                ('jobId', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('organizations', models.CharField(max_length=255)),
                ('department', models.CharField(max_length=64)),
                ('applicant', models.TextField()),
                ('status', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collectId', models.CharField(unique=True, max_length=64)),
                ('jobId', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('organizations', models.CharField(max_length=255)),
                ('department', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('status', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=64)),
                ('uid', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jobId', models.CharField(unique=True, max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('department', models.CharField(max_length=64)),
                ('number', models.CharField(default=b'0', max_length=10)),
                ('description', models.TextField()),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationsInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(unique=True, max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('name', models.CharField(default=None, max_length=255)),
                ('logoUrl', models.CharField(max_length=255)),
                ('bannerImageUrl', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('collegeId', models.CharField(max_length=11)),
                ('universityId', models.CharField(max_length=11)),
                ('provincesId', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Provinces',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='ReceResume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receResumeId', models.CharField(unique=True, max_length=64)),
                ('department', models.CharField(max_length=255)),
                ('jobId', models.CharField(max_length=64)),
                ('resumeId', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('sex', models.CharField(max_length=64)),
                ('college', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phoneNumber', models.CharField(max_length=20)),
                ('experience', models.TextField()),
                ('strong', models.TextField()),
                ('others', models.TextField()),
                ('status', models.CharField(max_length=20)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('organizationsId', models.ForeignKey(to='website.OrganizationsInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resumeId', models.CharField(unique=True, max_length=64)),
                ('account', models.CharField(unique=True, max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('sex', models.CharField(default=b'undefine', max_length=64, choices=[(b'undefine', '\u672a\u5b9a\u4e49'), (b'male', '\u7537'), (b'female', '\u5973')])),
                ('college', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phoneNumber', models.CharField(max_length=20)),
                ('experience', models.TextField()),
                ('strong', models.TextField()),
                ('others', models.TextField()),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(unique=True, max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('name', models.CharField(default=None, max_length=255)),
                ('iconUrl', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('collegeId', models.CharField(max_length=11)),
                ('universityId', models.CharField(max_length=11)),
                ('provincesId', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=64)),
                ('pid', models.CharField(max_length=11)),
            ],
        ),
        migrations.AddField(
            model_name='resume',
            name='studentInfoId',
            field=models.OneToOneField(to='website.StudentInfo'),
        ),
        migrations.AddField(
            model_name='jobs',
            name='organizationsId',
            field=models.ForeignKey(to='website.OrganizationsInfo'),
        ),
        migrations.AddField(
            model_name='collect',
            name='studentInfoId',
            field=models.ForeignKey(to='website.StudentInfo'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='studentInfoId',
            field=models.ForeignKey(to='website.StudentInfo'),
        ),
    ]
