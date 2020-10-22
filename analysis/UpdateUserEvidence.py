# -*- coding:utf-8 -*-
#@Time : 2020/8/10 0010 10:32
#@Author: Joword
#@File : UpdateUserEvidence.py

import os
import openpyxl as ol
from collections import Counter
from WriterExcel import *

class UpdateUserEvidence(object):
    u'''
    2020年8月10日，lisa需求：将海燕小姐姐、娜娜、lisa、方芳、陈晓玲、嘉乐的数据提供给怀瑾，估计是更新耳聋127Panel，鉴于之前
    就已经有过一次需要数据库数据然后提供给换进的经验，估计往后可能依旧会有，遂写成一个类，方便以后复用，
    逻辑：
    1、处理重复数据
    2、将数据转为字典以方便数据处理
    3、excel输出
    4、主函数逻辑
    时至23：03分完成，虽耗时一天，但收获颇丰，毕。
    '''
    def __init__(self,fileName=None):
        self.file = fileName

    def sort_element(self,arg):
        return arg[0]

    def duplicate_data(self,arg):
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
        list1 = list(set(no_duplicate)-set(duplicate))
        return no_duplicate,duplicate,list1


    def to_dict(self,arg,arg1,arg2):
        u'''
        :param arg:
        :param arg1:
        :param arg2:
        :return: 返回
        '''
        dict1 = []
        dict2 = []
        for variant in set(arg):
            temp = []
            for name in arg1:
                if variant + '|' + name in arg2.keys():
                    dict1.append(variant + '|' + name + '|' + arg2[variant + '|' + name])
                    temp.append(variant + '|' + name + '|' + arg2[variant + '|' + name])
            dict2.append(temp)
        return dict1,dict2

    def write_excel(self,arg,text=None):
        u'''
        :param arg:列表序列
        :param text: 保存文档名字
        :return: 输出函数
        '''
        wb = ol.Workbook()
        wa = wb.active
        wa.title = "data"
        wa['A1'],wa['B1'],wa['C1']="VariantId","Submitter(s)","Interpretation"

        for each in arg:
            wa.append(each)
        wb.save(text)

    def main(self):
        u'''
        主函数，仍有许多可优化的地方
        :return:
        '''
        with open(self.file,"r",encoding='utf-8') as f:
            next(f)
            lines = [i.strip().split("\t") for i in f]
            submitters = list({line[-2].upper():line[0] for line in lines}.keys())
            variantId_sames = {line[0]+"|"+line[-2].upper():line[-1] for line in lines}
            variantId_all,variant_rest = self.duplicate_data(variantId_sames.keys())[0],self.duplicate_data(variantId_sames.keys())[1]
            variantId_no_duplicate = list(set(variantId_all) - (set(variantId_all) & set(variant_rest)))
            variantId_duplicate = list(variant_rest)+list(set(variantId_all) & set(variant_rest))
            variant_unique = self.to_dict(variantId_duplicate, submitters, variantId_sames)
            # variant_count = {i:variantId_duplicate.count(i) for i in variantId_duplicate if variantId_duplicate.count(i) > 1}
            # max_number = Counter(variantId_duplicate).most_common(1)[0][1]
            variant_duplicate_list = []
            variant_unique_list = [[str(i).split("|")[0],str(i).split("|")[1],str(i).split("|")[2]] for i in self.to_dict(variantId_no_duplicate, submitters, variantId_sames)[0]]
            for variants in variant_unique[1]:
                if len(variants) == 2:
                    variant2 = [str(variants[0]).split("|")[0], str(variants[0]).split("|")[1]+"/"+str(variants[1]).split("|")[1], str(variants[0]).split("|")[2]+"/"+str(variants[1]).split("|")[2]]
                    variant_duplicate_list.append(variant2)
                if len(variants) == 3:
                    variant3 =[str(variants[0]).split("|")[0], str(variants[0]).split("|")[1]+"/"+str(variants[1]).split("|")[1]+"/"+str(variants[2]).split("|")[1], str(variants[2]).split("|")[2]+"/"+str(variants[2]).split("|")[2]+"/"+str(variants[2]).split("|")[2]]
                    variant_duplicate_list.append(variant3)
                if len(variants) == 4:
                    variant4 =[str(variants[0]).split("|")[0], str(variants[0]).split("|")[1]+"/"+str(variants[1]).split("|")[1]+"/"+str(variants[2]).split("|")[1]+"/"+str(variants[3]).split("|")[1], str(variants[0]).split("|")[2]+"/"+str(variants[1]).split("|")[2]+"/"+str(variants[2]).split("|")[2]+"/"+str(variants[3]).split("|")[2]]
                    variant_duplicate_list.append(variant4)
            variant_list = variant_unique_list+variant_duplicate_list
            variant_list.sort()
            self.write_excel(variant_list,"result.xlsx")

# if __name__ == '__main__':
#     test = UpdateUserEvidence("data.txt")
#     test.main()