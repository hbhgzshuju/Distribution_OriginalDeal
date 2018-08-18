# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 11:19:34 2017

@author: cwl
"""

#import pandas as pd
#Data_original = pd.read_excel(u'e:\\data\\1.xlsx',sheetname = 0,keep_default_na = False)

#Data_freedom = pd.read_excel(u'e:\\data\\杂\\27届定类.xlsx',sheetname = 1)
#Data_freedom[u'序号'] = Data_freedom[u'序号'].fillna(method = 'ffill')
#Data_freedom = Data_freedom.fillna('')

#item = 11
#Index_data = Data_freedom[Data_freedom[u'序号'] == item].index
#Data = Data_freedom.loc[Index_data]
#Data_condition = Data.loc[Data.index[0]]

class Index_Deal(object):
    def __init__(self,Data):
        self.Data = Data
    
    def Condition_Summary(self):
        Conditions = []
        for condition in self.Data.index:
            Data_condition = self.Data.loc[condition]
            Conditions.append(self.Condition_Deal(Data_condition ))
    
        if len(Conditions) != 1:
            Result_conditions = ' & '.join(Conditions)
        else:
            Result_conditions = Conditions[0]
        
        return(Result_conditions)

    def Condition_Deal(self,Data_condition):
        ##个性化筛选,不同要求对应不同条编码##
        Columns_condition = u'(Data_original["' + Data_condition[u'字段'] + '"]'
        
        if Data_condition[u'包含|不包含|等于|不等于'] == u'包含':
            Condition = Columns_condition + u'.str.contains("' + Data_condition[u'关键字'] + '"))'
        elif Data_condition[u'包含|不包含|等于|不等于'] == u'不包含':
            Condition = u'~' + Columns_condition + u'.str.contains("' + Data_condition[u'关键字'] + '"))'
        elif Data_condition[u'包含|不包含|等于|不等于'] == u'等于':
            Condition = Columns_condition + u'=="' + Data_condition[u'关键字'] + '")'
        elif Data_condition[u'包含|不包含|等于|不等于'] == u'不等于':
            Condition = Columns_condition + u'!="' + Data_condition[u'关键字'] + '")'
        else:
            Condition = Columns_condition + ')' + '!=' + Columns_condition + ')'
    
        return(Condition)



#Data_operation = Data.loc[Data.index[0]]

class Typeticket_Deal(object):
    """个性化操作"""
    def __init__(self,Data_original,Data,Index_need):
        
        self.Data_original = Data_original
        self.Data_operation = Data.loc[Data.index[0]]
        self.Index_need = Index_need
    
    def Operation_Summary(self):
        
        Type_ticket = self.Operation_Deal(self.Data_original,self.Data_operation,self.Index_need)
    
        return(Type_ticket)
    
    def Operation_Deal(self,Data_original,Data_operation,Index_need):
        ##一次电话内容个性化操作##
        Column_operation = u'一次电话内容'
        
        if Data_operation[u'模糊替换|精确替换|暴力替换|前面增加|后面增加'] == u'模糊替换':
            Data_original.loc[Index_need,[Column_operation]] = Data_original.loc[Index_need,[Column_operation]].replace(Data_operation[u'关键字1'],Data_operation[u'关键字2'],regex = True)
        elif Data_operation[u'模糊替换|精确替换|暴力替换|前面增加|后面增加'] == u'精确替换':
            Data_original.loc[Index_need,[Column_operation]] = Data_original.loc[Index_need,[Column_operation]].replace(Data_operation[u'关键字1'],Data_operation[u'关键字2'])
        elif Data_operation[u'模糊替换|精确替换|暴力替换|前面增加|后面增加'] == u'暴力替换':
            Data_original.loc[Index_need,[Column_operation]] = Data_operation[u'关键字1']
        elif Data_operation[u'模糊替换|精确替换|暴力替换|前面增加|后面增加'] == u'前面增加':
            Data_original.loc[Index_need,[Column_operation]] = Data_operation[u'关键字1'] + Data_original.loc[Index_need,[Column_operation]]
        elif Data_operation[u'模糊替换|精确替换|暴力替换|前面增加|后面增加'] == u'后面增加':
            Data_original.loc[Index_need,[Column_operation]] = Data_original.loc[Index_need,[Column_operation]] + Data_operation[u'关键字1']
        else:
            pass
        
        Type_ticket = Data_original[Column_operation].values
        
        return(Type_ticket)


def Nominal_Freedom(Data_original,Data_freedom):
    
    Levels_freedom = Data_freedom[u'序号'].drop_duplicates()
    for freedom in Levels_freedom:
        try:
            Index_data = Data_freedom[Data_freedom[u'序号'] == freedom].index
            Data = Data_freedom.loc[Index_data]
            Index_need = Data_original[eval(Index_Deal(Data).Condition_Summary())].index
            Data_original.loc[:,u'一次电话内容'] = Typeticket_Deal(Data_original,Data,Index_need).Operation_Summary()
        except:
            print(u'序号:' + str(freedom) + u'出错')
            
    return(Data_original[u'一次电话内容'].values)

#Data_original = pd.read_excel(u'e:\\data\\杂\\定类-个性化测试1.xlsx',sheetname = 0,keep_default_na = False)
#Type_ticket = Nominal_Freedom(Data_original,Data_freedom)
#Data_original.loc[:,[u'一次电话内容']] = Type_ticket
#Data_original.to_excel(u'e:\\data\\2.xlsx',encoding = 'gb18030',index = False)
