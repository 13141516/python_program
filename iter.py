'''
Created on Sep 13, 2016

@author: chenli
'''
#Iterator && Iterable 比较
#1.Iterator类需要重写__iter__,__next__而Iterable类只需要重写__iter__。
#2.for循环时，对于Iterator对象会调用__next__,而Iterable对象则是借助于yield(本例)。

from _collections_abc import Iterable, Iterator
from builtins import isinstance

'''
this is a demo of object of Iterable
'''
class RecIterable(object):
    def __init__(self, n):
        self.i = 0
        self.n = n
        
    def __generator(self):
        while self.i < self.n:
            yield self.i
            self.i += 1
            
    def __iter__(self):
        return self.__generator()

'''
this is a demo of object of Iterator
'''
class RecIterator(object):
    def __init__(self, n):
        self.i = 0
        self.n = n
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.i < self.n:
            self.i += 1
            return self.i - 1
        else:
            raise StopIteration
            
if __name__ == '__main__':
    recIterable = RecIterable(3)
    recIterator = RecIterator(3)
    print("recIterable is Iterable %s" % isinstance(recIterable, Iterable))
    print("recIterable is Iterator %s" % isinstance(recIterable, Iterator))
    print("recIterable is Iterable %s" % isinstance(recIterator, Iterable))
    print("recIterable is Iterator %s" % isinstance(recIterator, Iterator))
    for recIterableItem in recIterable.__iter__():
        print(recIterableItem)
    for recIteratorItem in recIterator:
        print(recIteratorItem)