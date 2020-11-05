# -*- coding:utf-8 -*-
# @Time : 2020/11/4 0004 10:43
# @Author: Joword
# @File : ReferenceCrawler.py

import re
import sys
import json
import random
import logging
import requests
import mysql.connector as mc
from pyquery import PyQuery as pq
from sshtunnel import SSHTunnelForwarder

u'''
鉴于耳聋自动化解读报告需要出具PMID对应的参考文献格式，实现思路如下：
**同时考虑怀瑾需要随时使用此程序进行参考文献导出
1、连接数据库，获取参考文献的PMID
2、将这些PMID做成参数导入，https://pubmed.ncbi.nlm.nih.gov/+PMID/citations,
*注意到数据库中存在NBK格式PMID，遂https://www.ncbi.nlm.nih.gov/books/+NBKPMID/，中作抓取CITE结果
3、再将CITE结果存入172服务器中即可,后续再布置
'''

class ReferenceFormatCrawler(object):
	
	def __init__(self, host: str, user: str, passwd: str, database: str):
		u'''ReferenceFormatCrawler(host="192.168.29.37",user="vardecoder",passwd="Decoder#123",database="varDecoding")
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
		self.__DOMAIN_GOOGLE = 'https://pubmed.ncbi.nlm.nih.gov/'
		self.__URL_GOOGLE_SEARCH = "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=2&num={num}&tbs=qdr:all%2Ccdr:1%2Ccd_min:{start_date}%2Ccd_max:{end_date}&lr={language_result}"
	
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
		return getattr(ReferenceFormatCrawler, item) if item in [self.host, self.user, self.passwd,
																 self.database] else "Can not find the attribute."
	
	def __setattr__(self, key, value):
		return setattr(ReferenceFormatCrawler, key, value)
	
	def __delattr__(self, item):
		pass
	
	def __repr__(self):
		return "host:{}, port:{}, user:{}, password:{}, database_name:{}".format(self.host, self.__port, self.user,
																				 self.passwd, self.database)
	
	def __del__(self):
		pass
	
	@staticmethod
	def pq_html(content):
		return pq(content)
	
	@property
	def user_agent(self):
		with open("google_user_agents.txt", "r") as f:
			return [i.strip().split("\n")[0] for i in f.readlines()]
	
	def to_select(self, table_name: str) -> str:
		u'''
		:param table_name: 数据库表名
		:return: SQL
		'''
		return "SELECT * FROM {}".format(str(table_name))
	
	def select_tables_data(self, select_sql: str) -> list:
		u'''通过SQL语句提取出对应表的数据
		:param select_sql: 包含数据库中对应表的数据
		:return: 该表中所有列的数据列表
		'''
		result = list()
		with SSHTunnelForwarder((self.host, 22), ssh_username='vardecoder', ssh_password='VarDecoder',
								remote_bind_address=('0.0.0.0', 3306)) as server:
			try:
				connect = mc.connect(host="127.0.0.1", port=server.local_bind_port, user=self.user, passwd=self.passwd,
									 database=self.database)
				cursor = connect.cursor()
				cursor.execute(select_sql)
				result = cursor.fetchall()
			except:
				connect.rollback()
			finally:
				connect.close()
				return result
	
	def get_pmid(self, old_pmid: list, new_pmid: list) -> list:
		u'''共计292762篇，统计自2020年11月4日
		:param old_pmid:旧的pmids list
		:param new_pmid: 新的pmids list
		:return: 去重后的pmids list
		'''
		pmid_list = list()
		for old in old_pmid:
			if "," not in old[1]:
				pmid_list.append(old[1])
			else:
				pmid_list.extend(str(old[1]).split(","))
		new_list = [i[1] for i in new_pmid]
		return list(set(pmid_list + new_list))
	
	def get_pubmed_pmid(self, pmids:list)->list:
		u'''main function
		Parameters
		----------
		pmids pmid list
		e.g query = 'https://pubmed.ncbi.nlm.nih.gov/22520757/citations/'
		query_NBK ='https://www.ncbi.nlm.nih.gov/books/NBK368474/'
		
		Returns [{pmid:references},{},...]
		-------

		'''
		result=[]
		pmid_all_number = ['https://pubmed.ncbi.nlm.nih.gov/'+str(i)+'/citations/' for i in pmids if re.match('\d+',i,re.I)]
		pmid_NBK = ['https://www.ncbi.nlm.nih.gov/books/'+str(i) for i in pmids if re.match('NBK\d+',i,re.I)]
		pmid_full = pmid_all_number+pmid_NBK
		headers = {'User-Agent': random.choice(self.user_agent)}
		for pmid in pmid_full:
			try:
				if re.match('NBK',str(pmid).split("/")[-1],re.I):
					requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
					request_result = requests.get(url=pmid, headers=headers, timeout=150)
					pq_text = self.pq_html(request_result.text.encode('utf-8'))
					result.append({str(pmid).split("/")[-1]:pq_text('.bk_tt').text()})
				else:
					request_result = requests.get(url=pmid, headers=headers, timeout=150)
					pq_text = self.pq_html(request_result.text)
					citation_dict = json.loads(pq_text('p').text())
					citation_index = str(citation_dict['id']).split("pmid:")[1]
					citation_orig = str(citation_dict['nlm']['orig']).split(". PMID:")[0]+'.'
					citation_format = str(citation_dict['nlm']['format']).split(". PMID:")[0]+'.'
					result.append({citation_index:"|".join([citation_orig,citation_format])})
					logging.info(pmid+'has the citation.')
			except:
				logging.info(pmid+'has not the citation.')
				
		return result
		

# if __name__ == '__main__':
# 	logging.basicConfig(filename='reference_crawler.log', filemode='a',
# 						format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
# 						datefmt='%Y-%m-%d %H:%M:%S')
# 	test = ReferenceFormatCrawler(host="192.168.29.37", user="vardecoder", passwd="Decoder#123", database="varDecoding")
# 	old_sql = test.to_select("variant_literature")
# 	new_sql = test.to_select("new_literature_information_temp")
# 	old_pmid = test.select_tables_data(old_sql)
# 	new_pmid = test.select_tables_data(new_sql)
# 	pmids = test.get_pmid(old_pmid, new_pmid)
# 	pmid_dict = test.get_pubmed_pmid(pmids)
