#coding:utf8
__author__ = 'fenton-fd.zhu'


'''
单例模板，继承，装饰器都可以
'''

class Singleton(object):
    '''
    继承自本类，就是单例
    '''
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            obj = super(Singleton, cls);
            cls._instance = obj.__new__(cls, *args, **kwargs);
            return cls._instance;

#装饰器版本单例
def singleton(cls, *args, **kwargs):
    _instance = {};
    def wrapper():
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs);
        return _instance[cls];
    return wrapper;

