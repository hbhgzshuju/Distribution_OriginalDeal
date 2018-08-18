# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 17:22:27 2017

@author: cwl
"""

import pandas as pd
#import File_Read

#Data_original = pd.read_excel(u'e:\\data\\匹配-婚博会id测试.xlsx',
#                              sheetname = 0,
#                              convesters = {u'婚博会id':str},
#                              keep_default_na = False)

#Data_original[u'婚博会id'] = Data_original[u'婚博会id'].astype(str)


#Data_research_loveid = pd.read_excel(u'e:\\data\\匹配测试.xlsx',convesters = {u'婚博会id':str})
#Data_research_loveid[u'婚博会id'] = Data_research_loveid[u'婚博会id'].astype(str)

#Data_result = pd.merge(Data_original,Data_research_loveid,how = 'left',left_on = u'婚博会id',right_on = u'婚博会id')


#Data_original,Data_research_loveid必须包含婚博会id字段

class Match_Loveid(object):
    """调研项匹配-婚博会id"""
    def __init__(self,Data_original,Data_research_loveid):
        
        self.Data_original = Data_original
        self.Data_research_loveid = Data_research_loveid.drop_duplicates(u'婚博会id')
        
    def Summary_Deal(self):
        ##汇总##
        self.Data_original,self.Data_research_loveid = self.Fotmat_Deal(self.Data_original,self.Data_research_loveid)
        Data_result = self.Match_Just(self.Data_original,self.Data_research_loveid)

        List_original = self.Data_original.columns.tolist()
        List_need = self.Data_research_loveid.columns.tolist()
        List_need.remove(u'婚博会id')        
        
        for column in List_need:
            if column in List_original:
                Data_result = self.Match_exits(Data_result,column)
            else:
                pass
        
        return(Data_result)
    
    def Fotmat_Deal(self,Data_original,Data_research_loveid):
        ##格式处理##
        Data_original[u'婚博会id'] = Data_original[u'婚博会id'].astype(str)
        Data_research_loveid[u'婚博会id'] = Data_research_loveid[u'婚博会id'].astype(str)

        return(Data_original,Data_research_loveid)
    
    def Match_Just(self,Data_original,Data_research_loveid):
        ##左连接##
        Data_result = pd.merge(Data_original,Data_research_loveid,how = 'left',left_on = u'婚博会id',right_on = u'婚博会id')
        
        return(Data_result)
    
    def Match_exits(self,Data_result,column):
        ##Data_original存在调研项处理##
        column_x = column + u'_x'
        column_y = column + u'_y'
        
        Index_need = Data_result[~(Data_result[column_y].isnull())].index
        Data_result.loc[Index_need,[column_x]] = Data_result.iloc[Index_need][column_y]
        
        del Data_result[column_y]
        
        Data_result = Data_result.rename(columns = {column_x:column})
        
        return(Data_result)

#Data_result = Match_Loveid(Data_original,Data_research_loveid).Summary_Deal()

#Data_result.to_excel(u'e:\\data\\1.xlsx',encoding = '18030')
