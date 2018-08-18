# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 17:16:14 2017

@author: cwl
"""

#import pandas as pd

#Data_original = pd.read_excel(u'e:\\data\\杂\\20171201一遍数据源1830.xlsx',
#                              sheetname = 0,
#                           keep_default_na = False)

#Data_priority = pd.read_excel(u'E:\\python\\Distribution_OriginalDeal\\Distribution_OriginalDeal-5.9\\定类优先级\\27届定类1.xlsx',
 #                             sheetname = 0)
#Data_priority[u'展会类型'] = Data_priority[u'展会类型'].fillna(method = 'ffill')
#Data_priority[u'展会'] = Data_priority[u'展会'].fillna(method = 'ffill')

#Data = Data_original.iloc[1]

##输入定类表和数据源
##数据源包括"本届索票信息","一次电话内容","展会类型","身份等级"

#Data_aim = Data_original.loc[Index_part1 + Index_part2]

class Nominal_New(object):
    """定类-新会员"""
    def __init__(self,Data_priority):
        self.Data_priority = Data_priority
    
    def Summary_Deal(self,Data):
        ##汇总##
        Type_ticket = Data[u'本届索票信息'].split('+')
        if len(Type_ticket) == 1:
            Nominal = self.Nominal_One(Type_ticket,self.Data_priority)
        elif len(Type_ticket) >= 2:
            Nominal = self.Nominal_More(Type_ticket,self.Data_priority)
        else:
            Nominal = Type_ticket
        
        return(Nominal)
        
    def Nominal_One(self,Type_ticket,Data_priority):
        ##定类-单次索票##
        Priority = Data_priority[Data_priority[u'本届索票信息'] == Type_ticket[0]]
        Nominal = Priority[u'类型'].values[0]
        
        return(Nominal)
    
    def Nominal_More(self,Type_ticket,Data_priority):
        ##定类-多次索票##
        
        Index_priority = []
        for item in Type_ticket:
            Index_priority = Index_priority + Data_priority[Data_priority[u'本届索票信息'] == item].index.tolist()
        
        Index_min = min(Index_priority)
        
        #判定多重展
        Index_removes = Data_priority[Data_priority[u'本届索票信息'].str.contains(u'.*?第2步没完成')].index.tolist()
        Index_removes = Index_removes + Data_priority[Data_priority[u'本届索票信息'].str.contains(u'.*?第1步没完成')].index.tolist()
        for Index_remove in Index_removes:
            try:
                Index_priority.remove(Index_remove)
            except:
                pass
        
        Exhibitions = Data_priority.loc[Index_priority,[u'展会类型']].drop_duplicates()
        
        if len(Exhibitions) >= 2:
            Multiple = u'-多重展'
        else:
            Multiple = u''

        Nominal = Data_priority.loc[Index_min,[u'类型']].values[0] + Multiple

        return(Nominal)

#Nominal_New(Data_priority).Summary_Deal(Data)


class Nominal_Comeback(object):
    """定类-回归"""
    def __init__(self,Data_priority):
        self.Data_priority = Data_priority
        
    def Summary_Deal(self,Data):
        ##汇总##
        Index_priority,Exhibition_end = self.Exhibition_Deal(Data,self.Data_priority)
        
        #if (Exhibition_end == u'回归-珠宝展') or (Exhibition_end == u'回归-旅游展'):
        #    Identity = ''
        #else:
        Identity = self.Identity_Deal(Data,self.Data_priority)
        
        Multiple = self.Exhibitions_Deal(Index_priority,self.Data_priority)
    
        Nominal = Exhibition_end + Identity + Multiple
        
        return(Nominal)
    
    def Exhibition_Deal(self,Data,Data_priority):
        ##判定展会##
        Type_ticket = Data[u'本届索票信息'].split('+')
        Index_priority = []
        for item in Type_ticket:
            Index_priority = Index_priority + Data_priority[Data_priority[u'本届索票信息'] == item].index.tolist()
        
        Index_min = min(Index_priority)
        Exhibition = Data_priority.loc[Index_min,[u'展会']].values[0]
        
        #儿博会展会类型非儿博会和母婴展，增加"-其他展"
        #if (Exhibition == u'儿博会') and (Data[u'定类展会'] != u'儿博会') and (Data[u'定类展会'] != u'母婴展') and (Data[u'定类展会'] != ''):
        #    Exhibition_end = Exhibition + u'-其他展-回归-'        
        #珠宝展和旅游展需在回归后面加相应的珠宝展和旅游展
        #elif (Exhibition == u'珠宝展') or ((Exhibition == u'旅游展')):
        #    Exhibition_end = u'回归-' + Exhibition
        #婚博会直接回归-
        #elif Exhibition == u'婚博会':
        #    Exhibition_end = u'回归-'
        #只剩下家博会,-回归-给他
        #else:
        Exhibition_end = Exhibition + u'-回归-'
        
        return(Index_priority,Exhibition_end)
        
    def Identity_Deal(self,Data,Data_priority):
        ##等级判断##
        Dict_identity = {u'金卡':u'金卡',
                         u'vip':u'VIP',
                         u'老会员':u'老会员'}
        
        Identity = Dict_identity[Data[u'身份等级']]

        return(Identity)
    
    def Exhibitions_Deal(self,Index_priority,Data_priority):
        ##多重展判断##

        #Index_removes = Data_priority[Data_priority[u'本届索票信息'].str.contains(u'.*?第2步没完成')].index.tolist()
        #Index_removes = Index_removes + Data_priority[Data_priority[u'本届索票信息'].str.contains(u'.*?第1步没完成')].index.tolist()
        #for Index_remove in Index_removes:
        #    try:
        #        Index_priority.remove(Index_remove)
        #    except:
        #        pass
        
        Exhibitions = Data_priority.loc[Index_priority,[u'展会类型']].drop_duplicates()
        if len(Exhibitions) >= 2:
            Multiple = u'-多重展'
        else:
            Multiple = ''        
    
        return(Multiple)
        

#Nominal_Comeback(Data_priority).Summary_Deal(Data)


class Nominal_Summary(object):
    """定类汇总"""
    def __init__(self,Data_priority):
        self.Data_priority = Data_priority
    
    def Summary_Deal(self,Data_original):
        ##定类##
        
        
        Columns_need = [u'身份等级',u'本届索票信息',u'一次电话内容']
        Data_Nominal = Data_original[Columns_need].drop_duplicates()
        Data_Nominal[u'一次电话内容'] = Data_Nominal.apply(self.Critical_Deal,axis = 1)
        
        for item in range(len(Data_Nominal)):
            Item = Data_Nominal.iloc[item]
            Index_nominal = Data_original[(Data_original[u'身份等级'] == Item[u'身份等级']) &\
                                          (Data_original[u'本届索票信息'] == Item[u'本届索票信息'])].index.tolist()
            
            Data_original.loc[Index_nominal,[u'一次电话内容']] = Item[u'一次电话内容']
        
        Nominals = Data_original[u'一次电话内容'].values.tolist()
        
        return(Nominals)
    
    def Critical_Deal(self,Data):
        
        try:
            if Data[u'身份等级'] == u'新会员':
                Nominal = Nominal_New(self.Data_priority).Summary_Deal(Data)
            else:
                Nominal = Nominal_Comeback(self.Data_priority).Summary_Deal(Data)
        except:
            Nominal = Data[u'一次电话内容']
        return(Nominal)

#import datetime
#Time_start = datetime.datetime.now()
#Data_result = Nominal_Summary(Data_priority).Summary_Deal(Data_aim)
#Data_aim[u'一次电话内容'] = Data_result
#End_start = datetime.datetime.now()
#print((End_start - Time_start).seconds)

#Columns_need = [u'身份等级',u'本届索票信息',u'定类展会',u'一次电话内容']
#Data_original.loc[Index_part1 + Index_part2,Columns_need].to_csv(u'e:\\data\\1.csv',encoding = 'gb18030',index = False)
#Data_original.to_excel(u'e:\\data\\1.xlsx',encoding = 'gb18030',index = False)
