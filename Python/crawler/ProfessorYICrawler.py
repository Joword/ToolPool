# -*- coding:utf-8 -*-
#@Time : 2020/11/9 0009 10:24
#@Author: Joword
#@File : ProfessorYICrawler.py




u'''
百度抓取
上海浦东新区、天津滨海新区、重庆两江新区、浙江舟山群岛新区、兰州新区、广州南沙新区、陕西西咸新区、贵州贵安新区、青岛西海岸新区、
大连金普新区、四川天府新区、湖南湘江新区、南京江北新区、福州新区、云南滇中新区、哈尔滨新区、长春新区、江西赣江新区、雄安新区
19个新区的土地面积、GDP、固定资产投资总额、城投企业名单
'''

import requests
from pyquery import PyQuery as pq

