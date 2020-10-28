# -*- coding:utf-8 -*-
#@Time : 2020/8/11 0011 9:14
#@Author: Joword
#@File : WriterExcel.py

try:
    import openpyxl as ol
except ImportError:
    raise ImportError("Can not find the openpyxl, Please, install it.")

class WriteExcel(object):

    def __init__(self,arg):
        self.arg = arg
        self.words = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    def reformat_name(self,fileName):
        if fileName.endswith(".xlsx"):
            return fileName
        else:
            return fileName.split(".")[0]+".xlsx"

    def to_excel(self,fileName,sheetName,header):
        wb = ol.Workbook()
        wa = wb.active
        wa.title = sheetName
        for i in range(len(header)):
            wa[self.words[i]+"1"] = header[i]

        for each in self.arg:
            wa.append(each)
        wb.save(self.reformat_name(fileName))