# -*- coding:utf-8 -*-
#@Time : 2020/11/13 0013 15:36
#@Author: Joword
#@File : StatisticDatabase.py

import re
import mysql.connector as mc
from sshtunnel import SSHTunnelForwarder

try:
	import openpyxl as ol
except ImportError:
	raise ImportError("Can not find the openpyxl, Please, install it.")


class StatisticDatabase(object):
	
	def __init__(self, host: str, user: str, passwd: str, database: str):
		u'''StatisticDatabase(host="192.168.29.37",user="vardecoder",passwd="Decoder#123",database="varDecoding")
		:param host: Internetworking Protocol address in database
		:param user: User name in database
		:param passwd: Password in database
		:param database: the name of database
		:param port: The protocol port of database, the default was 3306, it can be changed if need.
		The database default was MySQL, if you want others, you could change the arguments.
		'''
		self.host = host
		self.user = user
		self.passwd = passwd
		self.database = database
		self.__port = 3306
		self.model = None
		self.words = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
					  "T", "U", "V", "W", "X", "Y", "Z"]
	
	@property
	def get_port(self):
		return self.__port
	
	def set_port(self, port):
		u'''
		:param port: new port
		:return: to change the value of port
		'''
		self.__port = port
		print(self.__port)
	
	def __getattr__(self, item):
		return getattr(StatisticDatabase, item) if item in [self.host, self.user, self.passwd,
																self.database] else "Can not find the attribute."
	
	def __setattr__(self, key, value):
		return setattr(StatisticDatabase, key, value)
	
	def __delattr__(self, item):
		pass
	
	def __repr__(self):
		return "host:{}, port:{}, user:{}, password:{}, database_name:{}".format(self.host, self.__port, self.user,
																				 self.passwd, self.database)
	
	def __del__(self):
		pass
	
	def get_crud(self):
		return self._crud_word
	
	@property
	def _crud_word(self, sql: str) -> str:
		u'''使用正则表达式判断是进行了什么CRUD数据库操作
		:param sql: sql语句
		:return: 对应模式名称
		'''
		import re
		select_match = re.match(r'^SELECT', sql, re.I)
		single_merge_match = re.match(r'^SELECT.*LEFT JOIN', sql)
		crud = {"select": bool(select_match), "select merge": bool(single_merge_match)}
		key = [i for i in crud.keys() if crud[i] is True]
		return key[0]
	
	def isTables(self, table_name: str) -> dict:
		u'''判断数据库是否存在table_name
		:param table_name:数据库表名
		:return:True/False
		'''
		table_list = None
		with SSHTunnelForwarder((self.host, 22), ssh_username='vardecoder', ssh_password='VarDecoder',
								remote_bind_address=('0.0.0.0', 3306)) as server:
			try:
				connect = mc.connect(host="127.0.0.1", port=server.local_bind_port, user=self.user, passwd=self.passwd, database=self.database)
				cursor = connect.cursor()
				cursor.execute('show tables')
				table_lists = [i[0] for i in cursor.fetchall()]
				table_list = dict({i: False for i in table_lists if str(table_name) not in i},
								  **{i: True for i in table_lists if str(table_name) in i})
			except:
				connect.rollback()
			finally:
				connect.close()
				return table_list
	
	def to_select(self, table_name: str, conditions=None) -> str:
		u'''
		:param table_name: 数据库表名
		:param conditions: 筛选数据的条件
		:return:可能会有合并的情况和union搜索的存在，可能需要rewrite
		'''
		if conditions is None:
			return "SELECT * FROM {}".format(str(table_name))
		else:
			return "SELECT * FROM {} WHERE {}".format(str(table_name), str(conditions))
	
	def select_tables_data(self, select_sql: str) -> list:
		u'''通过SQL语句提取出对应表的数据
		:param select_sql: 包含数据库中对应表的数据
		:return: 该表中所有列的数据列表
		'''
		result = list()
		with SSHTunnelForwarder((self.host, 22), ssh_username='vardecoder', ssh_password='VarDecoder', remote_bind_address=('0.0.0.0', 3306)) as server:
			try:
				connect = mc.connect(host="127.0.0.1", port=server.local_bind_port, user=self.user, passwd=self.passwd, database=self.database)
				cursor = connect.cursor()
				table_name = select_sql.split("FROM")[1].split("WHERE")[0].strip() if 'WHERE' in select_sql else select_sql.split("FROM")[1].strip()
				if self.isTables(table_name)[table_name] is True:
					cursor.execute(select_sql)
					result = cursor.fetchall()
			except:
				connect.rollback()
			finally:
				connect.close()
				return result

if __name__ == '__main__':
	test = StatisticDatabase(host="192.168.29.37",user="vardecoder",passwd="Decoder#123",database="varDecoding")
	sql_user = test.to_select('user_collect')
	sql_sysmaster = test.to_select('sys_master')
	user_collect = test.select_tables_data(sql_user)
	sys_master = test.select_tables_data(sql_sysmaster)
	variantId = list(set([i[2] for i in user_collect] + [i[0] for i in sys_master]))
	gene = list(set([i[3] for i in user_collect] + [i[1] for i in sys_master]))
	print(len(variantId),len(gene))
	