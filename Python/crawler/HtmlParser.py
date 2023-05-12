# -*- coding:utf-8 -*-
# @Time : 2023/5/10 10:35
# @Author: Joword
# @File : 20230510.py
# @Software: PyCharm

import re
import itertools
from collections import Counter

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs


class HtmlParser(object):

    def __init__(self):
        self.contents = self.get_html("")
        self.tag_name = self.__tags()
        self.tag_total = self.__tags_total()
        self.parser()

    def __tags(self) -> list:
        return [[tag.name for tag in bs(self.contents[i], 'html.parser').find_all()] for i in range(len(self.contents))]

    def __tags_total(self) -> list:
        return list(set(itertools.chain.from_iterable([list(set(i)) for i in self.__tags()])))

    @staticmethod
    def get_html(path) -> list:
        import pandas as pd
        return pd.read_excel(path)['内容'].to_list()

    @classmethod
    def tags_desc(cls, label: str) -> str:
        values = {'table': ['table', 'tbody', 'td', 'tr', 'li', 'ol', 'ul'],
                  'dynamicData': ['v:imagedata', 'v:f', 'v:path', 'v:shapetype', 'o:lock', 'o:p', 'v:shape',
                                  'o:wrapblock', 'v:formulas', 'v:stroke'],
                  'image': ['img'], 'emphasize': ['br', 'u', 'h6', 'h2', 'font', 'sup', 'em', 'strong', 'del', 'hr'],
                  'link': ['a'],
                  'normal': ['p', 'div', 'span']}
        description = {'table': '表格标签', 'dynamicData': '动态数据标签', 'image': '图像标签',
                       'emphasize': '强调标签，包括换行、下划线、标题、字体、强调、删除、上标', 'link': '链接标签',
                       'normal': 'html结构标签'}

        return [description[k] for k,_ in values.items() if label in _][0]

    def table_replace(self, arg, kargs:dict, arg1:int) -> dict:
        replacement = str(arg)
        for k,i in enumerate(re.findall("<table.*?/table>", replacement, re.S)):
            replacement = replacement.replace(i, "@-@"+str(k))
        texts_plain = str(bs(replacement, 'html.parser').text)
        texts = str(bs(replacement, 'html.parser').text)
        for k,_ in enumerate(kargs['table']):
            texts_plain = texts_plain.replace("@-@"+str(k),str(_))
        text_strip = "\n".join([i for i in [txt.strip() for txt in texts.replace("\xa0"," ").split("\n") if txt.strip() != ""]])
        for _,j in enumerate(kargs['table']):
            text_strip = text_strip.replace("@-@" + str(_), str(kargs['lines'][_]))

        return {'text':texts_plain, 'texts':text_strip}

    def get_json(self,table,length=None) -> dict:
        df = [pd.read_html(i.prettify())[0].replace(np.nan, "~") for i in table.find_all("table")]
        lines = [[dict(i.T.to_dict()[j]) for j in i.T.to_dict()] for i in df]
        #     header = [df1.T.to_dict()[0][i] for i in df1.T.to_dict()[0].keys()]
        #     lines = [{header[k]:df1.T.to_dict()[i][k] for k,_ in enumerate(df1.T.to_dict()[i])} for i in range(1,len(df1.T.to_dict().keys()))]
        return {"lines": lines, "table":
            [pd.read_html(i.prettify())[0].replace(np.nan, "~").replace("\n","").replace("\xa0"," ") for i in table.find_all("table")]}

    def parser(self):
        texts, text = [],  []
        htmls = [bs(html, 'html.parser') for html in self.contents]
        df1 = pd.read_excel("")

        for idx,tag in enumerate(self.tag_name):
            if 'table' not in tag:
                texts.insert(idx,htmls[idx].text.replace("\n","").replace("\xa0"," "))
                text.insert(idx,"")
            else:
                texts.insert(idx,str(idx))
                text.insert(idx,str(idx))
                table_num = htmls[idx].find_all("table")
                result = self.get_json(htmls[idx], len(table_num))
                text_table = self.table_replace(htmls[idx],result,len(table_num))
                del texts[idx]
                texts.insert(idx,text_table['text'])
                del text[idx]
                text.insert(idx,text_table['texts'])
        df1['Html内容'] = texts
        df1['Parser内容'] = text


        df1.to_excel("result.xlsx",sheet_name="",index=False)


if __name__ == '__main__':
    test = HtmlParser()
