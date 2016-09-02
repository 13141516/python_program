# -*- coding: utf-8 -*-
# @author 852802020@qq.com
class UpperAttrMetaclass(type):
	def __new__(cls, name, bases, dct):
		attrs = ((name, value) for name, value in dct.items() if not name.startswith('__'))
		uppername_attr = dict((name.upper(), value) for name, value in attrs)
		return super(UpperAttrMetaclass, cls).__new__(cls, name, bases, uppername_attr)

class Xoo(object, metaclass=UpperAttrMetaclass):
	@property
	def score(self):
		return self.__score
	@score.setter
	def score(self, value):
		self.__score = value
	def fatbo():
		N = [1]
		while True:
			yield N
			N.append(0)
			N = [N[i-1] + N[i] for i in range(len(N))]
		
if __name__ == '__main__':
	print (dir(Xoo))
	'''
	xoo = Xoo()
	xoo.score = 100
	print(xoo.score)
	n = 0
	for value in Xoo.FATBO():
		print(value)
		n = n + 1
		if n == 10: 
			break
    '''