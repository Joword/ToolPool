# -*- coding:utf-8 -*-
#@Time : 2020/9/28 0028 17:57
#@Author: Joword
#@File : tool.py
# @update: 2020年10月22日

from WriterExcel import *
from collections import Counter

class tools(object):
	u'''工具大类：
	1、提供去除重复操作
	2、计数操作
	3、数据重构为字典形式
	'''
	def __init__(self,arg:str, margin):
		self.arg = arg
		self.margin = margin
		
	def handle_set(self,arg:str) -> dict:
		u'''若碰到想去重列表先做"|".join([])的操作
		:param arg:使用|分割的列表
		:return:去重并获得一个完整列表1与含有重复数据的列表2，并且若原列表有超过2个以上的元素，
		则列表1 与列表2有重复，返回列表1，列表2，以及列表1与列表2的差集
		'''
		no_duplicate = duplicate = []
		for i in arg:
			if str(i).split("|")[0] not in no_duplicate:
				no_duplicate.append(str(i).split("|")[0])
			else:
				duplicate.append(str(i).split("|")[0])
		list1 = list(set(no_duplicate) - set(duplicate))
		return {"no_duplicate":no_duplicate, "duplicate":duplicate, "intersection":list1}
	
	def count_number(self, count_list:list, margin=1) -> tuple:
		u'''
		:param count_list: 输入序列
		:param margin: 由Counter统计出来的出现次数
		:return: 默认返回margin = 1的结果，也可以修改
		'''
		counter = Counter(count_list)
		file1 = file2 = []
		for key in counter.keys():
			if counter[key] != margin:
				file1.append(key)
			else:
				file2.append(key)
		return file1,file2
	
	