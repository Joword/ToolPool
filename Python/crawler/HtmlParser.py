# -*- coding:utf-8 -*-
# @Time : 2023/5/10 10:35
# @Author: Joword
# @File : 20230510.py
# @Software: PyCharm

import itertools
from collections import Counter

import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup as bs


class HtmlParser(object):

    def __init__(self):
        self.contents = self.get_html("E:\\VIP-HL_update\\20230510\\HTML_客服-文档库_背景知识&产品介绍.xlsx")
        self.tag_name = self.__tags()
        self.tag_total = self.__tags_total()
        self.parser()

    def __tags(self):
        return [[tag.name for tag in bs(self.contents[i], 'html.parser').find_all()] for i in range(len(self.contents))]

    def __tags_total(self):
        return list(set(itertools.chain.from_iterable([list(set(i)) for i in self.__tags()])))

    @staticmethod
    def get_html(path):
        import pandas as pd
        return pd.read_excel(path)['内容'].to_list()

    @classmethod
    def tags_desc(cls, label: str):
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


    def parser(self):
        texts = []
        htmls = [bs(html, 'html.parser') for html in self.contents]

        print(pd.read_html(htmls[20].find_all("table")[0].prettify())[0])
        # print("|".join([i.replace("\xa0","-") for i in htmls[20].get_text("|").split("|")]))
        # for idx,tag in enumerate(self.tag_name):
        #     if 'table' not in tag:
        #         htmls[idx].text
        #     else:
        #         print(idx, htmls[idx].text)
        #         print()


if __name__ == '__main__':
    test = HtmlParser()
