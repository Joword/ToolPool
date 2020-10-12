# -*- coding:utf-8 -*-
#@Time : 2020/10/10 0010 10:14
#@Author: Joword
#@File : HandleDatabase.py

import re
import datetime
import pandas as pd
import mysql.connector as mc
from sshtunnel import SSHTunnelForwarder
from db.DatabaseAccess import DatabaseAccess

class HandleDatabase(DatabaseAccess):
	
	def get_index(self, fileName:str) -> list:
		u'''获取variantId
		:param fileName:文件名
		:return:variantId list
		'''
		df1 = pd.read_excel(fileName, index_col=0)
		return list(set(df1.index))
	
	def get_header(self, table_description:list)->list:
		return [i[0] for i in table_description]
	
	def database_tables_name(self, input_data:dict, table_name:str):
		u'''功用：根据criteria匹配数据库中pm3bp2,pp1bs4,pp4bp5,ps2pm6,ps3bs3,ps4，并返回是否匹配上
		:param table_name: 数据库中所需要匹配的表名
		:param input_data:输入数据
		:return:True/False
		'''
		pm3bp2_match = re.compile("PM3|BP2", re.I)
		pp1bs4_match = re.compile("PP1|BS4", re.I)
		pp4bp5_match = re.compile("PP4|BP5", re.I)
		ps2pm6_match = re.compile("PS2|PM6", re.I)
		ps3bs3_match = re.compile("PS3|BS3", re.I)
		ps4_match = re.compile("PS4", re.I)
		
		input_data['user_pm3bp2'] = True if pm3bp2_match.findall(input_data['criteria']) else False
		input_data['user_pm3bp2_match'] = True if pm3bp2_match.findall(table_name) else False
		input_data['user_pp1bs4'] = True if pp1bs4_match.findall(input_data['criteria']) else False
		input_data['user_pp1bs4_match'] = True if pp1bs4_match.findall(table_name) else False
		input_data['user_pp4bp5'] = True if pp4bp5_match.findall(input_data['criteria']) else False
		input_data['user_pp4bp5_match'] = True if pp4bp5_match.findall(table_name) else False
		input_data['user_ps2pm6'] = True if ps2pm6_match.findall(input_data['criteria']) else False
		input_data['user_ps2pm6_match'] = True if ps2pm6_match.findall(table_name) else False
		input_data['user_ps3bs3'] = True if ps3bs3_match.findall(input_data['criteria']) else False
		input_data['user_ps3bs3_match'] = True if ps3bs3_match.findall(table_name) else False
		input_data['user_ps4'] = True if ps4_match.findall(input_data['criteria']) else False
		input_data['user_ps4_match'] = True if ps4_match.findall(table_name) else False
		return input_data
		
	def select_database_data(self, table_name:str, conditions=None) -> dict:
		u'''连接数据库，做sql操作后拿到数据
		:param table_name: sql表名字
		:param conditions: 输入
		:return:
		'''
		with SSHTunnelForwarder(("192.168.29.37", 22), ssh_username='vardecoder', ssh_password='VarDecoder', remote_bind_address=('0.0.0.0', 3306)) as server:
			try:
				results, table_header = list(), list()
				connect = mc.connect(host="127.0.0.1", port=server.local_bind_port, user=self.user, passwd=self.passwd, database=self.database)
				cursor = connect.cursor()
				if isinstance(conditions,list) and isinstance(conditions[0],str):
					for i in conditions:
						cursor.execute('SELECT * FROM '+table_name+' WHERE variant_id=%s AND is_manual=%s', (str(i),int(2)))
						result = cursor.fetchall()
						table_header = self.get_header(cursor.description)
						results.append(list(result[0]))
				elif isinstance(conditions,list) and isinstance(conditions[0],dict):
					for i in conditions:
						evidences = list()
						labels = self.database_tables_name(i, table_name=table_name)
						cursor.execute("SELECT * FROM "+table_name+" WHERE variant_id=%s AND user_id=%s", (str(tuple(i.keys())[0]), int(i.get(tuple(i.keys())[0]))))
						result = cursor.fetchall()
						table_header = self.get_header(cursor.description)
						if len(result) > 0 and str(result[0][2].decode('utf-8'))==str(tuple(i.keys())[0]) and int(result[0][1]) == int(i.get(tuple(i.keys())[0])):
							if labels['user_pm3bp2'] is True and labels['user_pm3bp2_match'] is True:
								evidences = [i for i in result]
								results.append(list(evidences))
							elif labels['user_pp1bs4'] is True and labels['user_pp1bs4_match'] is True:
								evidences = [i for i in result]
								results.append(list(evidences))
							elif labels['user_pp4bp5'] is True and labels['user_pp4bp5_match'] is True:
								evidences = [i for i in result]
								results.append(list(evidences))
							elif labels['user_ps2pm6'] is True and labels['user_ps2pm6_match'] is True:
								evidences = [i for i in result]
								results.append(list(evidences))
							elif labels['user_ps3bs3'] is True and labels['user_ps3bs3_match'] is True:
								evidences = [i for i in result]
								results.append(list(evidences))
							elif labels['user_ps4'] is True and labels['user_ps4_match'] is True:
								evidences = [i for i in result]
								results.append(list(evidences))
							else:
								evidences=[i for i in result]
								results.append(list(evidences))
			except:
				connect.rollback()
			finally:
				connect.close()
				return {"header":table_header, "data":results}
		
	def insert_to_tables(self, table_name:str, data:dict):
		with SSHTunnelForwarder(("192.168.29.37",22), ssh_username='vardecoder', ssh_password='VarDecoder',remote_bind_address=('0.0.0.0',3306)) as server:
			try:
				connect = mc.connect(host="127.0.0.1", port=server.local_bind_port, user=self.user, passwd=self.passwd, database=self.database)
				cursor = connect.cursor()
				table_header = ",".join(data['header'])
				for contents in data['data']:
					for content in contents:
						sql = "INSERT INTO " + table_name+ "(" + table_header + ") VALUES ("+str("%s,"*len(data['header'])).strip(",")+")"
						cursor.execute(sql, tuple([content[i] for i in range(0,len(data['header']))]))
						connect.commit()
				print("The database was commited.")
			except:
				connect.rollback()
			finally:
				connect.close()
	
	def make_data(self):
		inputData,label_list,pm3bp2_data,pp1bs4_data,pp4bp5_data,ps2pm6_data,ps3bs3_data,ps4_data,user_evidence = list(),list(),list(),list(),list(),list(),list(),list(),list()
		#数据获取
		results = self.select_database_data("user_collect",self.get_index("50 discrepant variants.xlsx"))
		# 数据处理
		for content in results['data']:
			if content[10] is 2:
				label_dict = dict()
				label_dict[content[2]] = content[1]
				label_dict['criteria'] = content[8]
				label_dict['header'] = results['header']
				label_list.append(label_dict)
			content[0] = None
			content[1] = int(42)
			content[-4] = datetime.datetime.now()
			content[-2] = datetime.datetime.now()
			content = tuple(content)
			inputData.append(content)
		# pm3bp2 = self.select_database_data("user_pm3bp2",label_list)
		# pp1bs4 = self.select_database_data("user_pp1bs4",label_list)
		# pp4bp5 = self.select_database_data("user_pp4bp5",label_list)
		# ps3bs3 = self.select_database_data("user_ps3bs3", label_list)
		
		self.insert_to_tables(table_name="test", data=pm3bp2)
		
if __name__ == '__main__':
	test = HandleDatabase(host='192.168.29.37',user='vardecoder',passwd='Decoder#123',database='varDecoding')
	test.make_data()
	