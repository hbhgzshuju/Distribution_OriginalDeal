# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 18:27:04 2018

@author: cwl

E-mail: 1813528779@qq.com

To: Sharing and gratitude are my attitude towards life
"""

import pandas as pd

#Data_origin = pd.read_csv(u'e:\\data\\1.csv',encoding = 'gb18030',keep_default_na = False,dtype = str,low_memory = False)
#Data_recycle = pd.read_csv(u'e:\\data\\2.csv',encoding = 'gb18030',keep_default_na = False,dtype = str,low_memory = False)

class Recycle_Check(object):
    """回流检查"""
    def __init__(self,Data_origin,Data_recycle):
        
        self.Data_origin = Data_origin
        self.Data_recycle = Data_recycle

    def Recycle_Summary(self):
        
        Data_recycle_result = self.Recycle_Merge(self.Data_origin,self.Data_recycle)
        Data_origin,Data_recycle_result = self.Recycle_Judge(Data_recycle_result,self.Data_origin)
        
        return(Data_origin,Data_recycle_result)

    def Recycle_Merge(self,Data_origin,Data_recycle):
        
        Columns_need = [u'婚博会id',u'新郎手机',u'新娘手机',u'一次电话备注',u'一次电话内容',u'一次电话判定',u'一次电话分配日期',
                        u'二次电话备注',u'二次电话内容',u'二次电话判定',u'二次电话分配日期']
        
        Data_recycle_result = pd.merge(Data_recycle[Columns_need],
                               Data_origin[Columns_need],
                               how = 'left',
                               left_on = u'婚博会id',
                               right_on = u'婚博会id')
        
        
        
        for Column_need in Columns_need:
            Column_x = Column_need + u'_x'
            Column_y = Column_need + u'_y'
            Column_CC = Column_need + u'_CC'
            Column_Offline = Column_need + u'_Offline'
            
            Data_recycle_result = Data_recycle_result.rename(columns = {Column_x:Column_CC,Column_y:Column_Offline})
        
        
        Data_recycle_result[u'Check_FirstPhone'] = Data_recycle_result[u'一次电话判定_CC'] == Data_recycle_result[u'一次电话判定_Offline']
        Data_recycle_result[u'Check_SecondPhone'] = Data_recycle_result[u'二次电话判定_CC'] == Data_recycle_result[u'二次电话判定_Offline']
        
        for Item_replace in [u'一次电话备注_CC',u'一次电话备注_Offline',u'二次电话备注_CC',u'二次电话备注_Offline',]:
            Data_recycle_result[Item_replace] = Data_recycle_result[Item_replace].replace(u' ','',regex = True)
        
        return(Data_recycle_result)
    
    
    def Recycle_Judge(self,Data_recycle_result,Data_origin):
        
        Data_recycle_result[u'Recycle_Judge'] = u'一遍回流正常'
        #Allotdate_max_first = max(set(Data_recycle_result[u'一次电话分配日期_CC']))    
        Allotdate_max_second = max(set(Data_recycle_result[u'二次电话分配日期_CC']))
        
        Index_second = Data_recycle_result[Data_recycle_result[u'二次电话分配日期_CC'] == Allotdate_max_second].index
        Data_recycle_result.loc[Index_second,u'Recycle_Judge'] = u'二遍回流正常'
        #一遍回流检查
        Index_notjudge_first = Data_recycle_result[((Data_recycle_result[u'一次电话判定_Offline'] == u'未打')|(Data_recycle_result[u'一次电话判定_Offline'] == u'未通')|(Data_recycle_result[u'一次电话判定_Offline'] == u'')) &
                                                   (Data_recycle_result[u'Recycle_Judge'] == u'一遍回流正常')].index
    
        Data_notjudge_first = Data_recycle_result.loc[Index_notjudge_first]
        Index_abnormal_first1 = Data_notjudge_first[(Data_notjudge_first[u'一次电话判定_CC'] != u'未打')&(Data_notjudge_first[u'一次电话判定_CC'] != u'未通')].index
        Data_recycle_result.loc[Index_abnormal_first1,u'Recycle_Judge'] = u'一遍回流异常'
        Index_abnormal_first2 = Data_notjudge_first[((Data_notjudge_first[u'一次电话判定_CC'] == u'未打')|(Data_notjudge_first[u'一次电话判定_CC'] == u'未通')) &
                                                    (Data_notjudge_first[u'一次电话备注_CC'] != Data_notjudge_first[u'一次电话备注_Offline'])].index
    
        Data_recycle_result.loc[Index_abnormal_first2,u'Recycle_Judge'] = u'一遍回流异常'
        #二遍回流检查
        Index_notjudge_second = Data_recycle_result[((Data_recycle_result[u'二次电话判定_Offline'] == u'未打')|(Data_recycle_result[u'二次电话判定_Offline'] == u'未通')|(Data_recycle_result[u'二次电话判定_Offline'] == u'')) &
                                                    (Data_recycle_result[u'Recycle_Judge'] == u'二遍回流正常')].index
        
        Data_notjudge_second = Data_recycle_result.loc[Index_notjudge_second]
        Index_abnormal_second1 = Data_notjudge_second[(Data_notjudge_second[u'二次电话判定_CC'] != u'未打')&(Data_notjudge_second[u'二次电话判定_CC'] != u'未通')].index
        Data_recycle_result.loc[Index_abnormal_second1,u'Recycle_Judge'] = u'二遍回流异常'
        Index_abnormal_second2 = Data_notjudge_second[((Data_notjudge_second[u'二次电话判定_CC'] == u'未打')|(Data_notjudge_second[u'二次电话判定_CC'] == u'未通')) &
                                                      (Data_notjudge_second[u'二次电话备注_CC'] != Data_notjudge_second[u'二次电话备注_Offline'])].index
    
        Data_recycle_result.loc[Index_abnormal_second2,u'Recycle_Judge'] = u'二遍回流异常'    
        Data_recycle_result = Data_recycle_result.drop_duplicates(u'婚博会id')
        
        Data_origin = pd.merge(Data_origin,Data_recycle_result[[u'婚博会id',u'Recycle_Judge']],
                               how = 'left',
                               left_on = u'婚博会id',
                               right_on = u'婚博会id')
        
        Data_origin[u'Recycle_Judge'] = Data_origin[u'Recycle_Judge'].fillna('')
        
        return(Data_origin,Data_recycle_result)



#Data_origin,Data_recycle_result = Recycle_Check(Data_origin,Data_recycle).Recycle_Summary()
#Data_recycle_result.to_csv(u'e:\\data\\20180523回流检查.csv',encoding = 'gb18030',index = False)
#Data_recycle_result.to_excel(u'e:\\data\\20180606回流检查.xlsx',encoding = 'gb18030',index = False)