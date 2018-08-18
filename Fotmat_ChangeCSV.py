# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 10:22:31 2017

@author: cwl
"""

import win32com.client
#import pandas as pd
import os


class Fotmat_Change(object):
    def __init__(self,Dir_file):
        self.Dir_file = Dir_file
        self.Dir_change = os.getcwd() + os.sep + u'Station_transfer'
    
    def Summary_Deal(self):
        ##汇总##
        self.Critical_Deal(self.Dir_change)
        print(u'数据源Excel格式正在转为csv格式....')
        self.Read_Deal(self.Dir_file,self.Dir_change)
        print(u'数据源成功转为csv')
        
    def Read_Deal(self,Dir_file,Dir_change):
        ##xlsx转为csv##
        Excel = win32com.client.Dispatch('Excel.Application')
        Data_original = Excel.Workbooks.Open(Dir_file)
        Dir_save = Dir_change + os.sep + u'1.csv'
        Data_original.SaveAs(Dir_save,FileFormat = 6)
        Data_original.Close()
        Excel.Application.Quit()        
        
    def Critical_Deal(self,Dir_change):
        ##路径判断##
        if os.path.exists(Dir_change):
            pass
        else:
            os.mkdir(Dir_change)

#Dir = os.getcwd()
#Name_original = os.listdir(Dir + os.sep + u'数据源')[0]
#Dir_file = Dir + os.sep + u'数据源' + os.sep + Name_original
#Dir_file = u'e:\\data\\总表\\20171025冬季中国婚博会1030.xlsx'
#Fotmat_Change(Dir_file).Summary_Deal()
#Data = pd.read_csv(u'e:\\data\\1.csv',encoding = 'gb18030',converters = {u'新郎身份证号':str,u'新娘身份证号':str,})

