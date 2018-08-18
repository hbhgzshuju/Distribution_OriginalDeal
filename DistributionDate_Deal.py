# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 22:19:25 2017

@author: cwl
"""
import datetime


#Data_original必须包含分配天数
#Date_give给余量的日期
#Date_give = u'2017-11-15'
#import pandas as pd


#Data_original = pd.read_excel(u'e:\\data\\分配天数测试.xlsx',sheetname = 0,keep_default_na = False)
class DistributionDate_Deal(object):
    """分配天数处理"""
    def __init__(self,Data_original,Date_give):
        self.Data_original = Data_original
        self.Date_give = Date_give
    
    def Summary_Deal(self):
        ##汇总##
        Data_Distributiondate = self.Distributiondate_Deal(self.Data_original,self.Date_give)
        
        return(Data_Distributiondate)
        
    def Distributiondate_Deal(self,Data_original,Date_give):
        ##分配天数2暂时不打转2##
        Date_change_1 = datetime.datetime.strptime(Date_give,"%Y-%m-%d") + datetime.timedelta(days = -1)
        Date_change_2 = datetime.datetime.strptime(Date_give,"%Y-%m-%d") + datetime.timedelta(days = -2)
        
        
        Date_change_1 = datetime.datetime.strftime(Date_change_1,"%Y-%m-%d")
        Date_change_2 = datetime.datetime.strftime(Date_change_2,"%Y-%m-%d")
        
        Index_2_change = Data_original[(Data_original[u'分配天数'] == u'2暂时不打') &\
                                     (~((Data_original[u'一次电话分配日期'].str.contains(Date_change_1)) |
                                     (Data_original[u'一次电话分配日期'].str.contains(Date_change_2))))].index
        
        Data_original.loc[Index_2_change,[u'分配天数']] = '2'
        
        Index_2temp_change = Data_original[(Data_original[u'分配天数'] == u'2') &\
                                     ((Data_original[u'一次电话分配日期'].str.contains(Date_change_1)) |
                                     (Data_original[u'一次电话分配日期'].str.contains(Date_change_2)))].index
        
        Data_original.loc[Index_2temp_change,[u'分配天数']] = u'2暂时不打'

        Index_3_change = Data_original[(Data_original[u'分配天数'] != '0') &\
                                       (Data_original[u'分配天数'] != '1') &\
                                       (Data_original[u'分配天数'] != '2') &\
                                       (Data_original[u'分配天数'] != '3') &\
                                       (Data_original[u'分配天数'] != u'2暂时不打')].index
                                     
        Data_original.loc[Index_3_change,[u'分配天数']] = '3'
        
        Data_Distributiondate = Data_original[u'分配天数'].replace('','0')
        
        return(Data_Distributiondate)


#Data_original[u'分配天数'] = DistributionDate_Deal(Data_original,Date_give).Summary_Deal()
#Data_original.to_excel(u'e:\\data\\1.xlsx',encoding = 'gb18030',index = False)


