# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:17:04 2018

@author: cwl
"""

import pandas as pd
import datetime

#Data_original = pd.read_csv(u'e:\\data\\1.csv',encoding = 'gb18030',keep_default_na = False)
#Data_original = pd.read_excel(u'e:\\data\\Temp\\Temp_test1.xlsx',keep_default_na = False,sheet_name = 0)


#Pretreatment_Deal
class Pretreatment_Deal(object):
    
    def __init__(self,Data_original):
        
        self.Data_original = Data_original

    def Summary_Stage(self):
        
        self.Data_original = self.pretreatment_Stage(self.Data_original)
        
        return(self.Data_original)

    def pretreatment_Stage(self,Data_original):
        #阶段处理
        Data_original[u'一胎阶段'] = Data_original[u'一胎阶段'].replace(u'未知',u'')
        Data_original[u'二胎阶段'] = Data_original[u'二胎阶段'].replace(u'未知',u'')
        Data_original[u'三胎阶段'] = Data_original[u'三胎阶段'].replace(u'未知',u'')
        
        
        Index_empty = Data_original[(Data_original[u'一胎阶段'] =='') &\
                                    (Data_original[u'孕婴状态'] != '') &\
                                    (Data_original[u'孕婴状态'] != u'未知')].index
        
        Data_original.loc[Index_empty,u'一胎阶段'] = Data_original.loc[Index_empty,u'孕婴状态']
        
        Data_empty = Data_original.loc[Index_empty]
        
        #生日处理
        Index_huaiyun = Data_empty[(Data_empty[u'一胎阶段'] == u'怀孕') |
                                 (Data_empty[u'一胎阶段'] == u'备孕')].index
        
        Data_original.loc[Index_huaiyun,u'一胎生日'] = Data_original.loc[Index_huaiyun,u'预产期']
        
        Index_yichusheng = Data_empty[(Data_empty[u'一胎阶段'] == u'已出生') &
                                      ~(Data_empty[u'生日'].str.contains(u'[ －a-zA-Z年月日岁半底\+]')) &
                                      (Data_empty[u'生日'].str.contains(u'^\d{4}'))].index
        
        Data_original.loc[Index_yichusheng,u'一胎生日'] = Data_original.loc[Index_yichusheng,u'生日']
        
        for item in [u'一胎生日',u'二胎生日',u'三胎生日']:
            
            Data_original[item] = Data_original[item].replace('/','-',regex = True)
            for del_item in [u'，',u' ',u'－']:
                Data_original[item] = Data_original[item].replace(del_item,'',regex = True)
                
        
        #性别处理
        Index_sex_empty = Data_original[(Data_original[u'一胎性别'] == '') &\
                                     (Data_original[u'宝宝性别'] != '') &\
                                     (Data_original[u'宝宝性别'] != u'未知')].index
        
        Data_original[u'一胎性别'] = Data_original[u'一胎性别'].replace(u'未知',u'')
        Data_original.loc[Index_sex_empty,u'一胎性别'] = Data_original.loc[Index_sex_empty][u'宝宝性别']
    
        Data_original[u'一胎性别'] = Data_original[u'一胎性别'].replace(u'男',u'男宝')
        Data_original[u'一胎性别'] = Data_original[u'一胎性别'].replace(u'女',u'女宝')
        Data_original[u'一胎性别'] = Data_original[u'一胎性别'].replace(u'男女宝都有',u'男女都有')
        Data_original[u'一胎性别'] = Data_original[u'一胎性别'].replace(u'备孕or怀孕','')    
    
        return(Data_original)
    

#Data_result = Pretreatment_Deal(Data_original).Summary_Stage()

#Time_end = '2018-03-29'
#Column = u'一胎生日'

class Age_Deal(object):
    
    def __init__(self,Data_original):
        
        self.Data_original = Data_original
    
    def Age_Summary(self):
        
        Time_end = '2018-09-06'
        
        for Column in [u'一胎生日',u'二胎生日',u'三胎生日']:
            self.Data_original = self.Age_Count(self.Data_original,Column,Time_end)
            Column_year = u'年龄-' + Column
            self.Data_original[u'天数'] = self.Data_original[u'天数' + Column]
            self.Data_original[Column_year] = self.Data_original.apply(self.Birthday_Deal,axis = 1)
    
        return(self.Data_original)
        
    def Age_Count(self,Data_original,Column,Time_end):
    
        Column_need = u'辅助-' + Column
        Days_need = u'天数' + Column
        Data_original[Column_need] = ''
        
        
        Index_g = Data_original[Data_original[Column].str.endswith('-')].index
        Data_original.loc[Index_g,Column] = Data_original.loc[Index_g,Column] + '01'
        Index_del = Data_original[Data_original[Column].str.contains(u'[ －a-zA-Z年月日岁半底\+]')].index
        Data_original.loc[Index_del,Column] = u''
        
        Time_end = datetime.datetime.strptime(Time_end,"%Y-%m-%d")
        Data_original[Column_need] = pd.to_datetime(Data_original[Column])
        Data_original[Days_need] = Time_end - Data_original[Column_need]
        
        return(Data_original)
    
    def Birthday_Deal(self,Data):
        try:
            Year = str(int(Data[u'天数'].days/365))
        except:
            Year = ''
        
        return(Year)

#try:
#    Data_result = Age_Deal(Data_original).Age_Summary()
#except Exception,e:
#    print(e)

Column = u'一胎'

class Stage_Deal(object):

    def __init__(self,Data_original):
        
        self.Data_original = Data_original
    
    def Summary_Stage(self):
        
        for Column in [u'一胎',u'二胎',u'三胎']:
            self.Data_original = self.Stage_Each(self.Data_original,Column)
        
        self.Data_original = self.Stage_Belong(self.Data_original)
        
        return(self.Data_original)
            
    def Stage_Belong(self,Data_original):
        
        Data_original[u'阶段'] = ''
        for item in [u'【怀孕】',u'【大童】',u'【小童】']:
        
            Index_stage = Data_original[((Data_original[u'阶段-一胎'] == item) |
                                        (Data_original[u'阶段-二胎'] == item) |
                                        (Data_original[u'阶段-三胎'] == item)) &
                                        (Data_original[u'阶段'] == '')].index
        
            Data_original.loc[Index_stage,u'阶段'] = item
        
        return(Data_original)
        
    
    def Stage_Each(self,Data_original,Column):
    
        Column_stage = Column + u'阶段'
        Column_birth = u'年龄-' + Column + u'生日'
        Column_need = u'阶段-' + Column
        Data_original[Column_need] = ''
        
        Index_huaiyun = Data_original[Data_original[Column_stage] == u'怀孕'].index
        Data_original.loc[Index_huaiyun,Column_need] = u'【怀孕】'
        
        Index_beiyun = Data_original[Data_original[Column_stage] == u'备孕'].index
        Data_original.loc[Index_beiyun,Column_need] = u'【小童】'
        
        Index_yichusheng = Data_original[(Data_original[Column_stage] == u'已出生') &\
                                         (Data_original[Column_birth] != u'0') &\
                                         (Data_original[Column_birth] != u'1') &\
                                         (Data_original[Column_birth] != u'2') &\
                                         (Data_original[Column_birth] != '')].index
                                                 
        Data_original.loc[Index_yichusheng,Column_need] = u'【大童】'
        
        
        Index_stage_empty = Data_original[Data_original[Column_need] == ''].index
        Data_original.loc[Index_stage_empty,Column_need] = u'【小童】'

        return(Data_original)


def Main(Data_original):
    
    try:
        Data_result = Pretreatment_Deal(Data_original).Summary_Stage()
    except Exception as e:
        print(e)
    try:    
        Data_result = Age_Deal(Data_result).Age_Summary()
    except Exception as e:
        print(e)
    try:
        Data_result = Stage_Deal(Data_result).Summary_Stage()
    except Exception as e:
        print(e)
    
    return(Data_result)



#Data_original = pd.read_csv(u'e:\\data\\1.csv',encoding = 'gb18030',keep_default_na = False)
#Data_original.loc[:,[u'一胎阶段',u'一胎生日',u'一胎性别',u'阶段']] = Main()
#Data_original[u'一胎阶段'],Data_original[u'一胎生日'],Data_original[u'一胎性别'],Data_original[u'阶段'] = Main(Data_original)
#Data_result.to_excel(u'e:\\data\\1.xlsx',encoding = 'gb18030',index = False)
