'''
Created on Sep 5, 2016

@author: chenli
'''

#属性查找策略
#1.类中的属性X若是一个data descriptor的实例，则查找该属性时，会跳过__getattribute__，__getattr__，直接在data descriptor的__get__中查找。否则进入下一步。
#2.一般查找类的属性，调用的次序是类的__getattribute__，若找不到则调用是__getattr__，然后是父类的__getattribute__，__getattr__，依次循环。

#属性赋值策略
#1.查找obj.__class__.__dict__，如果attr存在并且是一个data descriptor，调用attr的data descriptor的__set__方法，结束。如果不存在，会继续到obj.__class__的父类和祖先类中查找，找到 data descriptor则调用其__set__方法。否则则进入下一步。
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
    m = Rec(height=15, width=100, length=18)
    print(m.getCapacity())
    print(r.getCapacity())
