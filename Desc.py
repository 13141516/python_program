'''
Created on Sep 5, 2016

@author: chenli
'''

#属性查找策略
#1.如果存在数据描述符则数据描述符得优先级是最高，并且从类属性开始查找数据描述符号.__get__,但是若查找的类的内建属性，则优先使用__getattribute__
#2.正常得属性则先从实例中查找，然后是是类，基类. __getattribute__,__getattr__,若找不到抛出异常
#属性赋值策略
#1.查找obj.__class__.__dict__，如果attr存在并且是一个data descriptor，调用attr的__set__方法，结束。如果不存在，会继续到obj.__class__的父类和祖先类中查找，找到 data descriptor则调用其__set__方法。没找到则进入下一步。
#2.直接在obj.__dict__中加入obj.__dict__['attr'] = value

from weakref import WeakKeyDictionary

class NonNegative(object):
    '''禁止<0被赋值'''
    def __init__(self, default):
        self.default = default
        self.data = WeakKeyDictionary()
 
    def __get__(self, instance, owner):
        '''instance 传递进来的对象，owner传递进来的类'''
        print('%s of %s __get is called' % (instance, owner))
        return self.data.get(instance, self.default)
 
    def __set__(self, instance, value):
        '''instance传递进来的对象'''
        print('%s of %s __set is called' % (instance, value))
        if value < 0:
            raise ValueError("Negative value not allowed: %s" % value)
        self.data[instance] = value
 
class Rec(object):
    __height = NonNegative(0)
    __width = NonNegative(0)
    __length = NonNegative(0)
    def __init__(self, **kw):
        self.__height = kw['height']
        self.__width = kw['width']
        self.__length = kw['length']
 
    def getCapacity(self):
        return self.__height*self.__width*self.__length
    
if __name__ == '__main__':
    r = Rec(height=15, width=10, length=18)
    print(r.getCapacity())
    m = Rec(height=15, width=100, length=18)
    print(m.getCapacity())
    print(r.getCapacity())