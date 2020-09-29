# -*- coding:utf-8 -*-
#@Time : 2020/9/28 0028 17:57
#@Author: Joword
#@File : tool.py

class tool(object):
	
	def __init__(self,arg:str):
		self.arg = arg
		
		
	def drop_duplicates(self,arg:str):
		u'''
		:param arg:
		:return:去重并获得一个完整列表1与含有重复数据的列表2，并且若原列表有超过2个以上的元素，
		则列表1 与列表2有重复，返回列表1，列表2，以及列表1与列表2的差集
		'''
		no_duplicate = []
		duplicate = []
		for i in arg:
			if str(i).split("|")[0] not in no_duplicate:
				no_duplicate.append(str(i).split("|")[0])
			else:
				duplicate.append(str(i).split("|")[0])
		list1 = list(set(no_duplicate) - set(duplicate))
		return no_duplicate, duplicate, list1