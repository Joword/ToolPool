# -*- coding:utf-8 -*-
#@Time : 2020/10/10 0010 10:14
#@Author: Joword
#@File : HandleDatabase.py
#@Update : Joword 2020/10/13 10:06

import re
import datetime
import pandas as pd
import openpyxl as ol
import mysql.connector as mc
from WriterExcel import *
from collections import Counter
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
	
	def make_data(self, input_data:dict)->tuple:
		u'''主要做数据修改
		:param input_data: SELECT得到的数据
		:return: 元组(未修改的字典型列表，已修改的字典型列表)
		'''
		label_list,output_data = list(),list()
		for content in input_data['data']:
			if content[10] is 2:
				label_dict = dict()
				label_dict[content[2]] = content[1]
				label_dict['criteria'] = content[8]
				label_dict['header'] = input_data['header']
				label_list.append(label_dict)
			content[0] = None
			content[1] = int(42)
			content[-4] = datetime.datetime.now()
			content[-2] = datetime.datetime.now()
			content = tuple(content)
			output_data.append(content)
		return label_list,output_data
	
	def database_tables_name(self, input_data:dict, table_name:str):
		u'''功用：根据criteria匹配数据库中pm3bp2,pp1bs4,pp4bp5,ps2pm6,ps3bs3,ps4，并返回是否匹配上，将criteria做匹配放到对应表
		名的字典字段中，同时也对数据库中表明做匹配放到数据库对应表名_match字段中
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
		u'''连接数据库，做sql操作后SELECT数据，经测试不可直接对SELECT数据操作，遂需分两步进行，并且为保证数据完整性，需要双循环
		
		:param table_name: sql表名字
		:param conditions: 输入条件
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
		# TODO:亮点是对需要单个写入的数据，进行批量写入
		u'''插入数据，在对拿到数据做处理后
		:param table_name: 数据库中表名
		:param data: 字典型数据
		:return: 无返回，需要try/except/finally关闭数据库否则会一直运行
		'''
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
	
	@property
	def select_group_users(self):
		groupName = 'ClinicalGroup'
		
		groupId,group_leader,group_member,informations,user_collect = int(),int(),list(),list(),list()
		with SSHTunnelForwarder(("192.168.29.37",22), ssh_username='vardecoder', ssh_password='VarDecoder',remote_bind_address=('0.0.0.0',3306)) as server:
			try:
				connect = mc.connect(host="127.0.0.1", port=server.local_bind_port, user=self.user, passwd=self.passwd, database=self.database)
				cursor = connect.cursor()
				
				groupIdSQL = "SELECT * FROM `group` WHERE group_name = "+"'"+groupName+"'"
				cursor.execute(groupIdSQL)
				group_data = cursor.fetchall()
				groupId = group_data[0][0]
				
				cursor.execute("SELECT * FROM user_collect WHERE user_id={} OR user_id={} OR user_id={} OR user_id={} OR user_id={} OR user_id={}".format(int(14),int(19),int(21),int(22),int(29),int(30)))
				user_collect = cursor.fetchall()
				
				cursor.execute("SELECT * FROM group_user WHERE group_id={}".format(int(groupId)))
				group_member = cursor.fetchall()
				for i in group_member:
					information = dict()
					cursor.execute("SELECT * FROM sys_user WHERE user_id={}".format(int(i[1])))
					user_name = cursor.fetchall()
					information['groupId'] = i[0]
					information['userId'] = i[1]
					information['name'] = str(user_name[0][2].decode('utf-8')).upper() + " " + str(user_name[0][1].decode('utf-8')).upper()
					informations.append(information)
			except:
				connect.rollback()
			finally:
				connect.close()
				return informations,user_collect
		
	
	def main(self):
		#TODO:新增新函数需重写
		u'''主程序入口
		:return:
		'''
		# # index数据获取
		# results = self.select_database_data("user_collect",self.get_index("50 discrepant variants.xlsx"))
		# # 数据处理
		# data_new = self.make_data(results)
		# # 数据修改
		# for table in ['user_pm3bp2','user_pp1bs4','user_pp4bp5','user_ps2pm6','user_ps3bs3','user_ps4']:
		# 	datas = self.select_database_data(table,data_new[0])
		# 	if len(datas['data']) > 0:
		# 		self.insert_to_tables(table_name="test",data=datas)
		
		u'''
		将user_collect表里所有的gene不分submitter地统计出总数
		'''
		information = dict()
		informations, user_collect = self.select_group_users[0],self.select_group_users[1]
		gene_list = [content[3] for content in user_collect]
		gene_list_counter = dict(Counter(gene_list))
		variant_list = [content[2] for content in user_collect]
		mix_compare = [content[3] + "|" + content[2] for content in user_collect]
		gene_variant = [{gene: ",".join([str(i).split("|")[1] for i in mix_compare if re.search(gene, i, re.I)]),"SUM": len([str(i).split("|")[1] for i in mix_compare if re.search(gene, i, re.I)])} for gene in gene_list_counter]
		
		u'''
		将user_collect的基因按照submitter统计出总数与variantId
		'''
		# for i in informations:
		# 	gene_list = [content[3] for content in user_collect if int(i['userId']) == int(content[1])]
		# 	gene_list_dict = dict(Counter(gene_list))
		# 	variant_list =[content[2] for content in user_collect if int(i['userId']) == int(content[1])]
		# 	mix_compare = [content[3]+"|"+content[2] for content in user_collect if int(i['userId']) == int(content[1])]
		# 	gene_variant = [{gene:",".join([str(i).split("|")[1] for i in mix_compare if re.search(gene,i,re.I)]),"SUM":len([str(i).split("|")[1] for i in mix_compare if re.search(gene,i,re.I)])} for gene in gene_list_dict]
		# 	information[i['name']] = gene_variant
			
		# with open("test.tsv","w+") as file:
		# 	# 输出文件
		# 	file.write("Gene"+"\t"+"Sum"+"\n")
		# 	for variant in gene_variant:
		# 		file.write(str(list(variant.keys())[0])+"\t"+str(variant[list(variant.keys())[1]])+"\t"+"\n")
			

# if __name__ == '__main__':
# 	test = HandleDatabase(host='192.168.29.37',user='vardecoder',passwd='Decoder#123',database='varDecoding')
# 	test.main()
	