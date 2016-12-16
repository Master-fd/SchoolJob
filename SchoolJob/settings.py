#coding:utf8
"""
Django settings for SchoolJob project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#网站地址

HOST = '119.29.151.45'
PORT = '8000'
DOMIN = 'www.schoolJon.com'
BASE_URL = 'http://127.0.0.1:8000/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k)&n7d_mfb(^%*u3p6-5$9#5+&(4@+b@6&&ap0745rv1d1gp3w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  #添加ajax 跨域请求 许可 中间件
    'website',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',   #cache中间件
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  #添加ajax 跨域请求 许可 中间件
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',   #cache中间件
)

ROOT_URLCONF = 'SchoolJob.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'website/templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SchoolJob.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'schoolJob',
        'HOST' : '119.29.151.45',
        'PORT' : '3306',
        'USER' : 'root',
        'PASSWORD' : '633922'
    }
}
# import redis_cache.backends.
#cache配置，使用redis做cache
CACHES = {
    'default' : {
        # 'BACKEND' : 'django.core.cache.backends.db.DatabaseCache',
        # 'BACKEND' : 'redis_cache.RedisCache',
        'BACKEND' : 'django.core.cache.backends.dummy.DummyCache',
        # 'LACATION' : '119.29.151.45:6379',
        # 'LACATION' : 'my_cache',
        'OPTIONS' : {
            'MAX_ENTRIES' : 1000,
            # 'DB' : 1,
            # 'PASSWORD' : '633922',   #没有密码，可以不用设置
            # 'PARSER_CLASS': 'redis.connection.HiredisParser',
            # 'CONNECTION_POOL_CLASS' : 'redis.BlockingConnectionPool',
            # 'CONNECTION_POOL_CLASS_KWARGS' : {
            #     'max_connections' : 50,
            #     'timeout' : 20,
            # }
        }
    }
}
CACHE_MIDDLEWARE_SECONDS = 0
CACHE_MIDDLEWARE_KEY_PREFIX = DOMIN





# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/ShangHai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CORS_ORIGIN_ALLOW_ALL = True   #允许所有跨域请求，具体查看https://github.com/ottoyiu/django-cors-headers/


#session不使用系统自带的，采用redis
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'  #引擎（默认）可选：文档、内存、数据库级别
SESSION_ENGINE = 'redis_sessions.session'  #使用redis做session引擎https://github.com/martinrusev/django-redis-sessions
SESSION_REDIS_HOST = '119.29.151.45'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0
# SESSION_REDIS_PASSWORD = '123456'    #如果redis没有设置密码，则不需要
SESSION_REDIS_PREFIX = DOMIN+'session'
SESSION_REDIS_SOCKET_TIMEOUT = 1
#cookie and session全局设置,
SESSION_COOKIE_NAME = 'session_id'      #Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串（默认
SESSION_COOKIE_PATH = '/'           #Session的cookie保存的路径（默认）
SESSION_COOKIE_DOMIN = None           #Session的cookie保存的域名（默认）
SESSION_COOKIE_AGE = 2000            #Session的cookie失效日期（默认2周）
SESSION_EXPIRE_AT_BROWSER_CLOSE = True    #是否关闭浏览器使得Session过期（默认）
SESSION_SAVE_EVERY_REQUEST = True   # 是否每次请求都保存Session，默认修改之后才保存（默认）