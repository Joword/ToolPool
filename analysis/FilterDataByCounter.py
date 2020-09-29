# -*- coding:utf-8 -*-
#@Time : 2020/8/26 0026 10:52
#@Author: Joword
#@File : FilterDataByCounter.py

from collections import Counter

class FilterData(object):
	
	def __init__(self,margin):
		self.margin = margin
	
	def count_number(self,name):
		u'''
	    使用Counter统计variantId总数，并筛选出超过1条数据的数据
	    :return:{超过1条数据},{只有1条数据}
	    '''
		with open(name, "r") as f1:
			lines = [i.strip().split("\t") for i in f1]
			variantId = [i[0] for i in lines]
			counter = Counter(variantId)
			file1, file2 = {}, {}
			for key in counter.keys():
				if counter[key] != self.margin:
					file1[key] = counter[key]
				else:
					file2[key] = counter[key]
			return file1, file2