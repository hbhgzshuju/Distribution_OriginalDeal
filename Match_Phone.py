# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 14:58:44 2017

@author: cwl
"""

#import File_Read
import pandas as pd

#Data_original = pd.read_excel(u'e:\\data\\杂\\匹配测试.xlsx',
#                           sheetname = 0,
#                           converters = {u'新郎手机':str,
#                                         u'新娘手机':str},
#                                         keep_default_na = False)

#Data_need = File_Read.File_Read().Research_phone_Read()



class Match_Phone(object):
    """调研项匹配-手机"""
    def __init__(self,Data_original,Data_need):
        self.Data_original = Data_original
        self.Data_need = Data_need
    
    def Match_Summary(self):
        ##汇总##
        self.Data_original,self.Data_need = self.Fotmat_Deal(self.Data_original,self.Data_need)
        Data_result = self.Match_Just(self.Data_original,self.Data_need)
        
        List_original = self.Data_original.columns.tolist()
        List_need = self.Data_need.columns.tolist()
        List_need.remove(u'手机号')
        
        for column in List_need:
            if column in List_original:
                Data_result = self.Match_Exists(Data_result,column)
            else:
                Data_result = self.Match_UnExists(Data_result,column)
        
        return(Data_result)
    
    def Fotmat_Deal(self,Data_original,Data_need):
        ##格式字符串##
        Data_original[u'新郎手机'] = Data_original[u'新郎手机'].astype(str)
        Data_original[u'新娘手机'] = Data_original[u'新娘手机'].astype(str)
        Data_need[u'手机号'] = Data_need[u'手机号'].astype(str)
        Data_need = Data_need.drop_duplicates(u'手机号')
        
        return(Data_original,Data_need)
        
    def Match_Just(self,Data_original,Data_need):
        ##手机匹配两次##
        Data_result = pd.merge(Data_original,Data_need,how = 'left',left_on = u'新郎手机',right_on = u'手机号')
        Data_result = pd.merge(Data_result,Data_need,how = 'left',left_on = u'新娘手机',right_on = u'手机号')
        
        del Data_result[u'手机号_x'],Data_result[u'手机号_y']
        
        return(Data_result)

    def Match_Exists(self,Data_result,column):
        ##存在调研项处理##
        column_x = column + u'_x'
        column_y = column + u'_y'
        
        for item in [column_y,column]:
            
            Index_need = Data_result[~Data_result[item].isnull()].index
            Data_result.loc[Index_need,[column_x]] = Data_result.iloc[Index_need][item].values
        
        del Data_result[column_y],Data_result[column]
        
        Data_result = Data_result.rename(columns = {column_x:column})
        
        return(Data_result)
    
    def Match_UnExists(self,Data_result,column):
        ##不存在调研项处理##
        column_x = column + u'_x'
        column_y = column + u'_y'
        
        Index_need = Data_result[~Data_result[column_y].isnull()].index
        Data_result.loc[Index_need,[column_x]] = Data_result.iloc[Index_need][column_y].values
        
        del Data_result[column_y]
        
        Data_result = Data_result.rename(columns = {column_x:column})
        
        return(Data_result)

#Data_result = Match_Phone(Data_original,Data_need).Match_Summary()
#Data_result.to_excel(u'e:\\data\\1.xlsx',encoding = 'gb18030',index = False)
