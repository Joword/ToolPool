# -*- coding:utf-8 -*-
#@Time : 2020/9/3 0003 10:49
#@Author: Joword
#@File : Database.py
#@Update: 2020/9/24


class Database(object):

	def __init__(self, host:str, user:str, passwd:str, database:str):
		u'''
		:param host:数据库IP
		:param user:数据库登陆用户名
		:param passwd:数据库登录密码
		:param database:数据库名字
		:param port:数据库端口,默认是3306，需要提前进行修改
		默认支持Mysql，若要SQLite/NoSQL等其他数据库需要重写
		:test Database(host="172.16.56.113",user="vardecoder",passwd="Decoder#123",database="varDecoding")
		'''
		self.host = host
		self.user = user
		self.passwd = passwd
		self.database = database
		self.__port = 3306
		self.model = None
	
	@property
	def get_port(self):
		return self.__port
	
	def set_port(self,port):
		self.__port = port
		print(self.__port)
	
	def __getattr__(self, item):
		return getattr(Database,item) if item in [self.host, self.user, self.passwd, self.database] else "Can not find the attribute."
	
	def __setattr__(self, key, value):
		return setattr(Database, key, value)
	
	def __delattr__(self, item):
		pass
	
	def __repr__(self):
		return "host:{}, port:{}, user:{}, password:{}, database_name:{}".format(self.host, self.__port, self.user, self.passwd, self.database)
	
	def __del__(self):
		pass
	
	def to_select(self, columns:str, table_name:str, conditions=None) -> str:
		u'''
		:param columns:数据库列名
		:param table_name: 数据库表名
		:param conditions: 筛选数据的条件
		:return:可能会有合并的情况和union搜索的存在，可能需要rewrite
		'''
		if conditions is None:
			return "SELECT {} FROM {}".format(columns,table_name)
		else:
			return "SELECT {} FROM {} WHERE {}".format(columns,table_name,conditions)
	
	def to_delete(self, table_name:str, column=None, value=None) -> str:
		u'''
		:param table_name:数据库中表名
		:param column: 数据库列名
		:param value: 删除的值
		:return: 慎用，会删除一条数据
		'''
		if column == value is None:
			return "DELETE {} FROM {}".format('*', table_name)
		else:
			return "DELETE {} FROM {} WHERE {}={}".format('*', table_name, column, value)
		
	def to_insert(self, table_name:str, columns=None, *args) -> str:
		u'''
		:param table_name:插入数据库表名
		:param columns: 插入数据库列名
		:param args:插入的一系列值
		:return:可能需要rewrite
		'''
		if columns is None:
			return "INSERT INTO {} VALUES {}".format(table_name, *args)
		else:
			return "INSERT INTO {}{} VALUES {}".format(table_name, columns, *args)

	def to_update(self, table_name:str, column1:str, column2:str, new_value=None, value=None) -> str:
		u'''
		:param table_name:数据库需要更新的表名
		:param column1:更新的数据库的列名1
		:param column2:更新数据库的条件列名
		:param new_value:更新数据库的列名1的值
		:param value:更新数据库条件列名的值
		:return:慎用，可能会有批量修改效应，难以Rollback
		'''
		return "UPDATE {} SET {}={} WHERE {}={}".format(table_name, column1, new_value, column2, value)
	
	def to_select_merge(self, columns:str, table_name_from:str, conditions_where:str, table_name_join:str, conditions_on:str) -> str:
		u'''
		:param columns:选择数据可用AS改别名
		:param table_name_from:数据库中数据FROM的表1
		:param conditions_where:FROM表1的条件，即WHERE条件
		:param table_name_join:合并表2
		:param conditions_on:合并表2条件，即ON条件
		:return:只可满足两表合并，如需多表合并要写多个LEFT JOIN，可能需要rewrite，在此之前，需要知道SQL的left join/right join/join的区别
		'''
		return "SELECT {} FROM {} LEFT JOIN {} ON {} WHERE {}".format(columns,table_name_from,table_name_join,conditions_on,conditions_where)
	
	@property
	def _crud_word(self,sql:str)->str:
		u'''使用正则表达式判断是进行了什么CRUD数据库操作
		:param sql: sql语句
		:return: 对应模式名称
		'''
		import re
		select_match = re.match(r'^SELECT',sql, re.I)
		delete_match = re.match(r'^DELETE',sql, re.I)
		update_match = re.match(r'^UPDATE',sql)
		insert_match = re.match(r'^INSERT',sql)
		single_merge_match = re.match(r'^SELECT.*LEFT JOIN',sql)
		crud = {"select":bool(select_match),"update":bool(update_match), "delete":bool(delete_match), "insert":bool(insert_match), "select merge":bool(single_merge_match)}
		key = [i for i in crud.keys() if crud[i] is True]
		return key[0]
		
	def connect(self, sql:str):
		u'''直接连接数据库，不通过其他通道连接数据库
		模式：select为SELECT，update为UPDATE，delete为DELETE，insert为INSERT，select merge为SELECT * FROM table_name LEFT JOIN * SET conditions WHERE conditions
		:param sql:进行不同的CRUD操作
		:return:返回序列化数据，根据arg选择要对数据进行对应的操作
		'''
		try:
			import mysql.connector as mc
		except ImportError:
			raise ImportError("Database.py need mysql.connect, Please manually install the modules about that.")
		self.model = self._crud_word
		connect = mc.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
		cursor = connect.cursor()
		cursor.execute(sql)
		result = cursor.fetchall()
		return result
		
	def _ssh_connect(self, ssh_ip:tuple, ssh_username:str, ssh_password:str, bind_address:tuple):
		try:
			from sshtunnel import SSHTunnelForwarder
		except ImportError:
			raise ImportError("The modules of sshtunel was not install, Please input 'pip install sshtunel' to install in command line.")
		try:
			import mysql.connector as mc
		except ImportError:
			raise ImportError("Database.py need mysql.connect, Please manually install the modules about that.")
		
		if self.host == ssh_ip:
			with SSHTunnelForwarder(ssh_ip, ssh_username=ssh_username, ssh_password=ssh_password, remote_bind_address=bind_address) as server:
				connect = mc.connect(host="127.0.0.1", port=server.local_bind_port, user=self.user, passwd=self.passwd, database=self.database)
				cursor = connect.cursor()
				cursor.execute("SELECT * FROM user_collect")
				result = cursor.fetchall()
				print(result)

# if __name__ == '__main__':
# 	test = Database(host="172.16.56.113",user="vardecoder",passwd="Decoder#123",database="varDecoding")
# 	sql = test.to_select("*","user_collect")
# 	test.connect(sql)
		