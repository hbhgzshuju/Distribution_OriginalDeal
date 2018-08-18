# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 22:12:48 2017

@author: cwl
"""

#import os
#import time
import pandas as pd
#import re
#import datetime


class Select_Deal(object):
    """数据选取"""
    def __init__(self,Data_original,Data_huifang):
        
        self.Data_original = Data_original
        self.Data_huifang = Data_huifang
    
    def Summary_Deal(self):
        ##汇总
        #print(u'正在筛选一遍数据源....')
        Index_part1 = self.Select_Part1(self.Data_original)
        Index_part2 = self.Select_Part2(self.Data_original)
        Index_part3 = self.Select_Part3(self.Data_original)
        Index_part4 = self.Select_Part4(self.Data_original,self.Data_huifang,
                                        Index_part1,Index_part2,Index_part3)

        #print(u'一遍数据源筛选完毕')
        
        return(Index_part1,Index_part2,Index_part3,Index_part4)

    def Select_Part1(self,Data_original):
        ##无效判定+未打未通+''
        #填写日期大于一次电话日期(为空也算)
        List_ineffectiveness = [u'未打',u'未通',u'暂无需求',u'北京索票',u'不来',
                                 u'筹备完毕',u'杭州索票',u'会员节-无效', u'婚博会-不来',u'活动无效',u'两天未通',
                                 u'三天未通',u'删除数据',u'双空错号',u'天津索票',u'勿扰',
                                 u'下届联系',u'下届无效',u'重复数据']
    
        Index_part11 = Data_original[(Data_original[u'一次电话判定'].str.contains('|'.join(List_ineffectiveness))) & \
                                         (Data_original[u'填写日期'] > Data_original[u'一次电话分配日期'])].index.tolist()        

        Index_part12 = Data_original[(Data_original[u'一次电话判定'] == '') & \
                                         (Data_original[u'填写日期'] > Data_original[u'一次电话分配日期'])].index.tolist()        
        
        Index_part1 = Index_part11 + Index_part12
        
        return(Index_part1)

    def Select_Part2(self,Data_original):
        ##未打未通非回访
        Index_part21 = Data_original[(Data_original[u'填写日期'] <= Data_original[u'一次电话分配日期']) & \
                                         (Data_original[u'一次电话判定'] == u'未通') & \
                                         (Data_original[u'本届索票信息'] != '')
                                         ].index.tolist()
        
        Index_part22 = Data_original[(Data_original[u'填写日期'] <= Data_original[u'一次电话分配日期']) & \
                                         (Data_original[u'一次电话判定'] == u'未打') & \
                                         (Data_original[u'本届索票信息'] != '')
                                         ].index.tolist()        

        Index_part23 = Data_original[(Data_original[u'填写日期'] <= Data_original[u'一次电话分配日期']) & \
                                         (Data_original[u'一次电话判定'].str.contains(u'活动结束|活动无效')) & \
                                         (Data_original[u'本届索票信息'] != '')
                                         ].index.tolist()
        
        Index_part2 = Index_part21 + Index_part22 + Index_part23
        
        return(Index_part2)
    
    def Select_Part3(self,Data_original):
        ##未打未通回访
        Index_part31 = Data_original[(Data_original[u'填写日期'] <= Data_original[u'一次电话分配日期']) & \
                                    (Data_original[u'本届索票信息'] == '') & \
                                    (Data_original[u'一次电话判定'] == u'未打')].index.tolist()
                                    
        Index_part32 = Data_original[(Data_original[u'填写日期'] <= Data_original[u'一次电话分配日期']) & \
                                    (Data_original[u'本届索票信息'] == '') & \
                                    (Data_original[u'一次电话判定'] == u'未通')].index.tolist()

        Index_part33 = Data_original[(Data_original[u'填写日期'] <= Data_original[u'一次电话分配日期']) & \
                                    (Data_original[u'本届索票信息'] == '') & \
                                    (Data_original[u'一次电话判定'].str.contains(u'活动结束|活动无效'))].index.tolist()
        
        Index_part3 = Index_part31 + Index_part32 + Index_part33
        
        return(Index_part3)
    
    def Select_Part4(self,Data_original,Data_huifang,
                     Index_part1,Index_part2,Index_part3):
        ##回访
        #除去已有索票的数据
        Index_part41 = pd.DataFrame(Data_original[Data_original[u'婚博会id'].isin(Data_huifang[u'婚博会id'])].index,columns = [u'索引'])
        Index_part123 = pd.DataFrame(Index_part1 + Index_part2 + Index_part3,columns = [u'索引'])
        Index_part42 = Index_part41[u'索引'][~Index_part41[u'索引'].isin(Index_part123[u'索引'])].values.tolist()
        
        Data_originalpart4 = Data_original.iloc[Index_part42]
        
        Index_part4 = Data_originalpart4[Data_originalpart4[u'一次电话判定'] == ''].index.tolist()
        
        return(Index_part4)
        
#if __name__ == '__main___':
#    Select_Deal()

#Index_part1,Index_part2,Index_part3,Index_part4 = Select_Deal(Data_original,Data_huifang).Summary_Deal()
#Index_part1 = Select_Deal(Data_original,Data_huifang).Select_Part1(Data_original)
#Index_part2 = Select_Deal(Data_original,Data_huifang).Select_Part2(Data_original)
#Index_part3 = Select_Deal(Data_original,Data_huifang).Select_Part3(Data_original)

#Data = Data_original.iloc[Index_part4]
#Data.to_excel(u'20171014测试结果2.xlsx',encoding = 'gb18030',index = False)
