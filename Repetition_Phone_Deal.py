# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 16:33:19 2018

@author: cwl

E-mail: 1813528779@qq.com

To: Sharing and gratitude are my attitude towards life
"""

#import pandas as pd

#Data_Origin = pd.read_csv(u'e:\\data\\1.csv',
#                            encoding = 'gb18030',
#                            keep_default_na = False,
#                            dtype = str)

#Index_test = Data_Origin[Data_Origin[u'一次电话判定'] != ''].index

#Data_Origin = Data_Origin.loc[Index_test]

def Phone_Value_Counts(Data_Origin):
    
    Index_groom_unempty = Data_Origin[Data_Origin[u'新郎手机'] != ''].index
    Index_bride_unempty = Data_Origin[Data_Origin[u'新娘手机'] != ''].index

    Phones = Data_Origin.loc[Index_groom_unempty,u'新郎手机'].append(Data_Origin.loc[Index_bride_unempty,u'新娘手机'])
    
    Phones_counts = Phones.value_counts()
    Phones_counts = Phones_counts[Phones_counts > 1]
    
    return(Phones_counts.index)

#Repetition = Phone_Value_Counts(Data_Origin)
