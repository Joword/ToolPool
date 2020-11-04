# -*- coding:utf-8 -*-
# @Time : 2020/11/4 0004 10:43
# @Author: Joword
# @File : ReferenceCrawler.py

import sys
import random
import requests
import mysql.connector as mc
from pyquery import PyQuery as pq
from sshtunnel import SSHTunnelForwarder

if sys.version_info[0] > 2:
	from urllib.parse import quote_plus, urlparse, parse_qs
else:
	from urllib import quote_plus
	from urlparse import urlparse, parse_qs

u'''
鉴于耳聋自动化解读报告需要出具PMID对应的参考文献格式，实现思路如下：
**同时考虑怀瑾需要随时使用此程序进行参考文献导出
1、连接数据库，获取参考文献的PMID
2、将这些PMID做成参数导入，https://pubmed.ncbi.nlm.nih.gov/+PMID,中作抓取CITE结果
3、再将CITE结果存入172服务器中即可
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
	
	def to_select(self, table_name: str, conditions=None) -> str:
		u'''
		:param table_name: 数据库表名
		:param conditions: 筛选数据的条件
		:return:可能会有合并的情况和union搜索的存在，可能需要rewrite
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
		u'''共计292762篇，
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
	
	def get_pubmed_pmid(self, pmids):
		# query = ['https://pubmed.ncbi.nlm.nih.gov/'+str(i)+'/' for i in pmids]
		query = 'https://pubmed.ncbi.nlm.nih.gov/22520757/'
		domain = self.__DOMAIN_GOOGLE
		url = query
		headers = {'User-gent': random.choice(self.user_agent)}
		requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
		request_result = requests.get(url=url, headers=headers, timeout=60)
		pq_content = self.pq_html(request_result.text)
		# TODO:print(pq_content('div:contains("22520757")').text())


if __name__ == '__main__':
	test = ReferenceFormatCrawler(host="192.168.29.37", user="vardecoder", passwd="Decoder#123", database="varDecoding")
	old_sql = test.to_select("variant_literature")
	new_sql = test.to_select("new_literature_information_temp")
	old_pmid = test.select_tables_data(old_sql)
	new_pmid = test.select_tables_data(new_sql)
	pmids = test.get_pmid(old_pmid, new_pmid)
	test.get_pubmed_pmid(pmids)
