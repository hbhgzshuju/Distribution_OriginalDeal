# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 14:47:11 2017

@author: cwl
"""

def Repetition_Deal(Data_original):
    ##处理重复号码##
    Index_delxinlang = Data_original[(Data_original[u'新郎手机'] == Data_original[u'新娘手机']) &\
                                    (Data_original[u'填写人'] == u'新郎')].index.tolist()
    
    Data_original.loc[Index_delxinlang,[u'新娘手机']]= ''
    
    Index_delxinlang = Data_original[(Data_original[u'新郎手机'] == Data_original[u'新娘手机']) &\
                                    (Data_original[u'填写人'] != u'新郎')].index.tolist()
    
    Data_original.loc[Index_delxinlang,[u'新郎手机']] = ''
    
    return(Data_original)

