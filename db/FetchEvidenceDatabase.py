# -*- coding:utf-8 -*-
#@Time : 2020/10/27 0027 14:26
#@Author: Joword
#@File : FetchEvidenceDatabase.py
#@updater: 2020年10月27日，192数据库提取user_pm3bp2/user_pp1bs4/user_pp4bp5/user_ps2pm6/user_ps3bs3/user_ps4表格数据.py

import re
import mysql.connector as mc
from sshtunnel import SSHTunnelForwarder

try:
    import openpyxl as ol
except ImportError:
    raise ImportError("Can not find the openpyxl, Please, install it.")

class FetchEvidenceDatabase(object):
    
    def __init__(self, host: str, user: str, passwd: str, database: str):
        u'''FetchEvidenceDatabase(host="192.168.29.37",user="vardecoder",passwd="Decoder#123",database="varDecoding")
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
        self.words = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    
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
        return getattr(FetchEvidenceDatabase, item) if item in [self.host, self.user, self.passwd,
                                                         self.database] else "Can not find the attribute."
    
    def __setattr__(self, key, value):
        return setattr(FetchEvidenceDatabase, key, value)
    
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
    
    def reformat_name(self, fileName) -> str:
        u'''检测输出的文件名是否为excel标准格式
        :param fileName: 输出文件名
        :return: 若文件名以.xlsx结尾，则返回文件名，若不以结尾则提取.前面的名字并赋以.xlsx
        '''
        if fileName.endswith(".xlsx"):
            return fileName
        else:
            return fileName.split(".")[0] + ".xlsx"
    
    def isTables(self, table_name: str) -> dict:
        u'''判断数据库是否存在table_name
        :param table_name:数据库表名
        :return:True/False
        '''
        table_list = None
        with SSHTunnelForwarder((self.host, 22), ssh_username='vardecoder', ssh_password='VarDecoder',
                                remote_bind_address=('0.0.0.0', 3306)) as server:
            try:
                connect = mc.connect(host="127.0.0.1", port=server.local_bind_port, user=self.user, passwd=self.passwd,
                                     database=self.database)
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

    def to_excel(self,contents:list, fileName:str, table_name:str, sheetName:str):
        u'''输出excel文件
        :param table_name: 数据库查询表名
        :param contents:输入列表
        :param fileName: 文件名,可以不用.xlsx结尾
        :param sheetName: 选项卡名字
        :return: None
        '''
        wb = ol.Workbook()
        wa = wb.active
        wa.title = sheetName
        new_eachs = []
        ILLEGAL_CHARACTER_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
        PM3BP2 = ['id','user_id','variant_id','amcg_name','publication_type','publication','strength','phase','inheritance','allele2','pathogenicity','pathogenicity_source','proband_num','points','evidence_sentence','comment','status','create_time','update_time']
        PP1BS4 = ['id','user_id','variant_id','acmg_name','publication_type','publication','strength','genotype','genotype_desc','phenotype','phenotype_desc','inheritance','affected_segregation','unaffected_segregation','non_segregation','lod_score_user','lod_score','case_num','figure','evidence_sentence','comment','status','create_time','update_time']
        PP4BP5 = ['id','user_id','variant_id','acmg_name','publication_type','publication','strength','phenotype','phenotype_omim_id','inheritance','proband_num','evidence_sentence','comment','status','create_time','update_time']
        PS2PM6 = ['id','user_id','variant_id','acmg_name','publication_type','publication','strength','de_novo_status','phenotype','phenotypic_consistency','proband_num','points','figure','evidence_sentence','comment','status','create_time','update_time']
        PS3BS3 = ['id','user_id','variant_id','acmg_name','publication_type','publication','strength','experiment','function_change','evidence_sentence','figure','comment','status','create_time','update_time']
        PS4 = ['id','user_id','variant_id','acmg_name','publication_type','publication','strength','inheritance','phenotype','ancestry','allele_in_patient','total_allele_in_patient','allele_in_control','total_allele_in_control','odds_ratio_user','odd_ratio','odds_ratio_lower','odds_ratio_upper','proband_num','p_value','evidence_sentence','comment','status','create_time','update_time']
        
        if table_name is 'user_pm3bp2':
            for pm3bp2s in range(len(PM3BP2)):
                wa[self.words[pm3bp2s]+"1"] = PM3BP2[pm3bp2s]
        elif table_name is 'user_pp1bs4':
            for pp1bs4s in range(len(PP1BS4)):
                wa[self.words[pp1bs4s]+'1'] = PP1BS4[pp1bs4s]
        elif table_name is 'user_pp4bp5':
            for pp4bp5s in range(len(PP4BP5)):
                wa[self.words[pp4bp5s]+"1"] = PP4BP5[pp4bp5s]
        elif table_name is 'user_ps2pm6':
            for ps2pm6s in range(len(PS2PM6)):
                wa[self.words[ps2pm6s]+"1"] = PS2PM6[ps2pm6s]
        elif table_name is 'user_ps3bs3':
            for ps3bs3s in range(len(PS3BS3)):
                wa[self.words[ps3bs3s]+"1"] = PS3BS3[ps3bs3s]
        elif table_name is 'user_ps4':
            for ps4s in range(len(PS4)):
                wa[self.words[ps4s]+"1"] = PS4[ps4s]
        
        for eachs in contents:
            temp = []
            for each in eachs:
                if type(each) is bytearray:
                    each = str(each.decode('utf-8'))
                    each = ILLEGAL_CHARACTER_RE.sub(r'',each)
                    temp.append(each)
                else:
                    each = ILLEGAL_CHARACTER_RE.sub(r'',str(each))
                    temp.append(str(each))
            new_eachs.append(temp)

        for i in new_eachs:
            wa.append(i)
        wb.save(self.reformat_name(fileName))
        
# if __name__ == '__main__':
#     test = FetchEvidenceDatabase(host='192.168.29.37', user='vardecoder', passwd='Decoder#123', database='varDecoding')
#     sql = test.to_select("user_ps4")
#     result = test.select_tables_data(sql)
#     test.to_excel(contents=result, fileName="ps4",table_name="user_ps4", sheetName="user_ps4")