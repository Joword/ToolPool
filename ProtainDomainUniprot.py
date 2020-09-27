# -*- coding:utf-8 -*-
# @Time : 2020/9/1 0001 9:47
# @Author: Joword
# @File : ProtainDomainUniprot.py

from collections import Counter
from WriterExcel import *


class OutputData(object):

    def __init__(self, arg):
        self.arg = arg

    def to_tsv(self, name: str):
        import pandas as pd
        df1 = pd.read_excel(name).drop_duplicates()
        save = df1.to_csv(name.split(".")[0] + ".tsv", sep='\t', index=None)

    def to_file(self, lists: list, output: str, sheetName: str, header: list):
        excel = WriteExcel(lists)
        return excel.to_excel(output, sheetName, header)

    def make_topology(self, name: str) -> list:
        u'''
        :param name:
        :return:特别处理病理数据，若要复用要加装饰器
        '''
        with open(name, "r", encoding='utf-8') as f:
            next(f)
            lines = [i.strip().split("\t") for i in f.readlines()]
            topology_list = []
            for line in lines:
                line[1] = "-".join(line[1].replace("\xa0", "").split("–"))
                topology_list.append({"value": line[0] + "|" + line[1] + "|" + line[2], "index": [
                                     str(i) for i in range(int(line[1].split("-")[0]), int(line[1].split("-")[1]) + 1)]})
            return topology_list

    def filter_same_data(self, dupLists: list, dupNames: list, submitter: int,
                         vipInterpretation: int, criteria: int, pp4Phenotype: int) -> list:
        u'''
        :param dupLists:参数1，重复的列表
        :param dupNames: 参数2，重复的index
        :param submitter: 参数3，输入用户所在列表的index
        :param vipInterpretation: 参数4，输入VIPHL所在列表的index
        :param criteria: 参数5，输入证据项所在列表的index
        :param pp4Phenotype: 参数6，输入PP4表型所在列表的index
        :return:
        '''
        data = []
        for name in dupNames:
            dup_list = [dup for dup in dupLists if dup[0] == name]
            if len(dup_list) == 2:
                temp_list1 = []
                temp_list1.extend(dup_list[0])
                temp_list1[submitter] = "/".join(
                    list(set([submitters[submitter] for submitters in dup_list])))
                temp_list1[vipInterpretation] = temp_list1[vipInterpretation] if temp_list1[vipInterpretation] == dup_list[
                    1][vipInterpretation] else temp_list1[vipInterpretation] + '/' + dup_list[1][vipInterpretation]
                temp_list1[criteria] = temp_list1[criteria] if temp_list1[criteria] == dup_list[
                    1][criteria] else temp_list1[criteria] + '/' + dup_list[1][criteria]
                temp_list1[pp4Phenotype] = temp_list1[pp4Phenotype] if temp_list1[pp4Phenotype] == dup_list[
                    1][pp4Phenotype] else temp_list1[pp4Phenotype] + '/' + dup_list[1][pp4Phenotype]
                data.append(temp_list1)
            else:
                temp_list2 = []
                temp_list2.extend(dup_list[0])
                temp_list2[submitter] = "/".join(
                    list(set([dup[submitter] for dup in dup_list])))
                temp_list2[vipInterpretation] = "/".join(
                    list(set([dup[vipInterpretation] for dup in dup_list])))
                temp_list2[criteria] = "/".join(
                    list(set([dup[criteria] for dup in dup_list])))
                temp_list2[pp4Phenotype] = "/".join(
                    list(set([dup[pp4Phenotype] for dup in dup_list])))
                data.append(temp_list2)
        return data

    def remove_duplicate(self, inputName: str, outputName: str):
        u'''
        :param inputName:输入文件名
        :param outputName: 输出文件名
        :return: 使用Counter计数，将列表划分为：重复列表、非重复列表。
        '''
        with open(inputName, "r", encoding='utf-8') as f:
            next(f)
            lines = [i.strip().split("\t") for i in f.readlines()]
            variantId = [line[0] for line in lines]
            dup_name = [name for name in Counter(
                variantId).keys() if Counter(variantId)[name] > 1]
            names = [name for name in Counter(
                variantId).keys() if Counter(variantId)[name] == 1]
            dup_lists = [line for line in lines if line[0] in dup_name]
            name_list = [line for line in lines if line[0] in names]
            data_list = self.filter_same_data(
                dup_lists,
                dup_name,
                submitter=1,
                vipInterpretation=8,
                criteria=12,
                pp4Phenotype=13)
            for k in (data_list + name_list):
                k[10] = '-' if k[10] == "0" else k[10]
                k[10] = 'one' if k[10] == "1" else k[10]
                k[10] = 'two' if k[10] == "2" else k[10]
                k[10] = 'three' if k[10] == "3" else k[10]
                k[10] = 'four' if k[10] == "4" else k[10]
                k[10] = "-" if k[10] == 'na' or k[10] == "" else k[10]
                k[11] = "-" if k[11] == 'na' or k[11] == "" else k[11]
                k[11] = str(float(k[11])) if k[11] != "-" else str(k[11])
            self.to_file(data_list + name_list,
                         outputName,
                         "Domain_GJB2",
                         ['variant_id',
                          'submitter',
                          'gene',
                          'cHGVS',
                          'pHGVS',
                          'Consequence',
                          'amino_acid',
                          'Clinvar_interpretation',
                          'auto_interpretation',
                          'Review',
                          'Stars',
                          'REVEL_score',
                          'Criteria',
                          'PP4_phenotype'])

    def make_file(self, outName: str) -> list:
        with open(outName, "r", encoding='utf-8') as f:
            next(f)
            lines = [i.strip().split("\t") for i in f.readlines()]
            topologies = make_topology()
            file_list = []
            for line in lines:
                list2 = []
                line[5] = str(line[5].replace("_", " "))
                line[5] = line[5].replace('"', '')
                line[9] = str(line[9].replace("_", " "))
                line[9] = str(line[9].replace('"', ''))
                line[11] = str(line[11].replace("na", "-"))
                line[12] = str(line[12].replace('"', ''))
                line[13] = str(line[13].replace('"', ''))
                line[10] = '-' if line[10] == "0" else line[10]
                line[10] = 'one' if line[10] == "1" else line[10]
                line[10] = 'two' if line[10] == "2" else line[10]
                line[10] = 'three' if line[10] == "3" else line[10]
                line[10] = 'four' if line[10] == "4" else line[10]
                if "-" not in line[6].split("/")[0]:
                    for topology in topologies:
                        if line[6].split("/")[0] in topology['index']:
                            list2.append(line + topology["value"].split("|"))
                else:
                    topology1 = [i["value"] for i in topologies if line[6].split(
                        "/")[0].split("-")[0] in i['index']]
                    topology2 = [i["value"] for i in topologies if line[6].split(
                        "/")[0].split("-")[1] in i['index']]
                    topologies_list = topology1 + topology2
                    if len(
                            topologies_list) > 0 and topologies_list[0] != topologies_list[1]:
                        feature_key = topologies_list[0].split(
                            "|")[0] + '/' + topologies_list[1].split("|")[0]
                        positions = topologies_list[0].split(
                            "|")[1] + '/' + topologies_list[1].split("|")[1]
                        description = topologies_list[0].split(
                            "|")[2] + '/' + topologies_list[1].split("|")[2]
                        list2.append(line +
                                     [feature_key, positions, description])
                    elif len(topologies_list) > 0 and topologies_list[0] == topologies_list[1]:
                        list2.append(line + topologies_list[0].split("|"))
                    elif len(topologies_list) == 0:
                        list2.append(line)

                if len(list2) > 0:
                    list2 = list2
                    file_list.append(list2[0])
                else:
                    file_list.append(line)

            return file_list


if __name__ == '__main__':
    test = OutputData([1, 2, 3])
    # test.remove_duplicate("protain_domain_gjb2.tsv","protain_domain_gjb2_no_dup.xlsx")
    # test = to_tsv("protain_domain_gjb2_no_dup.xlsx")
    # test1 = remove_duplicate("protain_domain_gjb2.tsv","protain_domain_gjb2_no_dup.xlsx")
    # test2 = make_file()
    # files = WriteExcel(test2)
    # files.to_excel("result.xlsx","GJB2",['VariantId', 'Submitter', 'Gene', 'cHGVS', 'pHGVS', 'Consequence', 'Amino acid', 'Clinvar interpretation', 'VIPHL interpretation', 'Review', 'Stars', 'REVEL score', 'Criteria', 'PP4 phenotype','Topology feature','Topology position(s)','Topology description'])
