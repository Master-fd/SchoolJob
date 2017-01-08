##SchoolJob 项目工程 Source Code##

**SchoolJob** 是一个专用于大学生社团纳新平台，学校社团注册之后，即可发布自己社团的相关纳新信息；新生们可以查看筛选查看该学校所有社团的相关纳新信息，收藏或发送自己的简历进行应聘；学校社团也可以方便的对简历进行管理，群发通知邮件。

###项目主要结构###
1、web 前端采用 jQuery 与 Sea.js 组件化开发。   
2、后台编程语言基于 Python2.7.12 ，主要使用的是 Django-1.8.4 开发，使用 Django 的 ORM 搭配 Mysql 储存数据。对应使用 Redis 保存热数据。   

###部署环境###
Django+uWSGI+nginx， 使用 Supervisor 进行 uWSGI 的后台进程管理 

