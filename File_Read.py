# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 22:11:03 2017

@author: cwl
"""


import os
import time
import pandas as pd
import Fotmat_ChangeCSV
#import re
#import datetime

class File_Read(object):
    """文件读取"""
    def __init__(self):
        Dir = os.getcwd()
        Name_original = os.listdir(Dir + os.sep + u'数据源')
        Name_priority = os.listdir(Dir + os.sep + u'定类优先级')
        Name_huifang = os.listdir(Dir + os.sep + u'ID_huifang')
        Name_research_phone = os.listdir(Dir + os.sep + u'Research_phone')
        Name_research_loveid = os.listdir(Dir + os.sep + u'Research_loveid')
        
        Name_separated = os.listdir(Dir + os.sep + u'Separated')    
        
        #过滤Thumbs.db缓冲文件名
        for item in [Name_original,Name_priority,Name_huifang,Name_research_phone,Name_research_loveid,Name_separated]:
            if u'Thumbs.db' in item:
                item = item.remove(u'Thumbs.db')
        
        self.Dir_original = Dir + os.sep + u'数据源' + os.sep + Name_original[0]
        self.Dir_priority = Dir + os.sep + u'定类优先级' + os.sep + Name_priority[0]
        self.Dir_huifang = Dir + os.sep + u'ID_huifang' + os.sep + Name_huifang[0]
        self.Dir_changeoriginal = Dir + os.sep + u'Station_transfer' + os.sep + u'1.csv'
        self.Dir_research_phone = Dir + os.sep + u'Research_phone' + os.sep + Name_research_phone[0]
        self.Dir_research_loveid = Dir + os.sep + u'Research_loveid' + os.sep + Name_research_loveid[0]
        self.Dir_separated = Dir + os.sep + u'Separated' + os.sep + Name_separated[0]
        
        
    def Original_Read(self):
        ##读取数据源##
        try:
            print(u'正在读取数据源....')
            try:
                os.remove(self.Dir_changeoriginal)
            except:
                pass
            
            if u'.csv' in self.Dir_original:
                Open_original = open(self.Dir_original,encoding = 'gb18030')
                Data_original = pd.read_csv(Open_original,keep_default_na = False,low_memory = False,dtype = str)
                Open_original.close()
            else:
                #由微软Excel装为csv再读取
                Fotmat_ChangeCSV.Fotmat_Change(self.Dir_original).Summary_Deal()
                Data_changeoriginal = open(self.Dir_changeoriginal,encoding = 'gb18030')
                
                Data_original = pd.read_csv(Data_changeoriginal,
                                              keep_default_na = False,
                                              #encoding = 'gb18030',
                                              low_memory = False,
                                              converters = {u'新郎身份证号':str,u'新娘身份证号':str,
                                                            u'分配天数':str,
                                                            #u'婚礼日期':str,
                                                            u'生日':str,u'预产期':str,
                                                            u'装修时间':str,u'一次快递单号':str,
                                                            u'一次快递时间':str,u'一次快递签收时间':str,
                                                            u'一胎生日':str,
                                                            u'二胎生日':str,
                                                            u'三胎生日':str,
                                                })
                
                
                Data_changeoriginal.close()
            
            try:
                os.remove(self.Dir_changeoriginal)
            except:
                pass
            
            
            print(u'数据源读取完毕')
        except:
            print(u'数据源读取失败,10秒后退出')
            time.sleep(10)
            exit()

        return(Data_original)
    
    def Priority_Read(self):
        ##读取数据源##
        try:
            print(u'正在读取定类优先级....')
            Data_priority = pd.read_excel(self.Dir_priority,
                                          sheetname = 0,
                                          )

            Data_priority[u'展会类型'] = Data_priority[u'展会类型'].fillna(method = 'ffill')
            Data_priority[u'展会'] = Data_priority[u'展会'].fillna(method = 'ffill')
            
            print(u'定类优先级读取完毕')
        except:
            print(u'定类优先级读取失败,10秒后退出')
            time.sleep(10)
            exit()

        return(Data_priority)    

    def Freedom_Read(self):
        ##读取数据源##
        try:
            print(u'正在读取个性化分型表....')
            Data_freedom = pd.read_excel(self.Dir_priority,
                                          sheetname = 1,
                                          converters = {u'序号':str}
                                          )

            
            Data_freedom[u'序号'] = Data_freedom[u'序号'].fillna(method = 'ffill')
            Data_freedom = Data_freedom.fillna('')

            print(u'个性化分型表读取完毕')
        except:
            print(u'个性化分型表读取失败,10秒后退出')
            time.sleep(10)
            exit()

        return(Data_freedom)

    def Huifang_Read(self):
        ##读取数据源##
        try:
            print(u'正在读取回访婚博会id....')
            Data_temp = open(self.Dir_huifang,encoding = 'gb18030')
            Data_huifang = pd.read_csv(Data_temp,
                                        #encoding = 'gb18030',
                                        converters = {u'婚博会id':str}
                                          )

            Data_temp.close()

            print(u'回访婚博会id读取完毕')
        except:
            print(u'回访婚博会id读取失败,10秒后退出')
            time.sleep(10)
            exit()

        return(Data_huifang)      
    
    def Research_phone_Read(self):
        ##读取数据源##
        try:
            print(u'正在读取调研项-手机....')
            Data_research_phone = pd.read_excel(self.Dir_research_phone,
                                   sheetname = 0,
                                   converters = {u'手机':str},
                                   #keep_default_na = False
                                          )
            
            print(u'调研项-手机读取完毕')
        except:
            print(u'调研项-手机读取失败,10秒后退出')
            time.sleep(10)
            exit()

        return(Data_research_phone)

    def Research_loveid_Read(self):
        ##读取数据源##
        try:
            print(u'正在读取调研项-婚博会id....')
            Data_research_loveid = pd.read_excel(self.Dir_research_loveid,
                                   sheetname = 0,
                                   converters = {u'婚博会id':str},
                                   #keep_default_na = False
                                          )
            
            print(u'调研项-婚博会id读取完毕')
        except:
            print(u'调研项-婚博会id读取失败,10秒后退出')
            time.sleep(10)
            exit()

        return(Data_research_loveid)

    def Separated_Read(self):
        ##读取数据源##
        try:
            print(u'正在读取隔开数据....')
            Data_separated = pd.read_excel(self.Dir_separated,
                                           sheetname = 0,
                                           keep_default_na = False
                                                  )
            
            print(u'隔开数据读取完毕')
        except:
            print(u'隔开数据失败,10秒后退出')
            time.sleep(10)
            exit()

        return(Data_separated)


class File_Read_Traversal(object):
    """文件读取"""
    def __init__(self,File_name):
        
        self.File_name = File_name

    def Origin_Read(self):
        ##读取数据源##
        try:
            #print(u'正在读取【',self.File_name,u'】文件夹数据....',sep = '')
            Name_origins = os.listdir(os.getcwd() + os.sep + self.File_name)
            if len(Name_origins) != 0:
                if u'Thumbs.db' in Name_origins:
                    Name_origins.remove(u'Thumbs.db')
                    
                Data_result = pd.DataFrame(columns = [u'婚博会id'])
                for Name_origin in Name_origins:
                    Dir_origin = os.getcwd() + os.sep + self.File_name + os.sep + Name_origin
                    if u'.csv' in Dir_origin:
                        Open_origin = open(Dir_origin,encoding = 'gb18030')
                        Data_origins = pd.read_csv(Open_origin,
                                                    keep_default_na = False,
                                                    low_memory = False,
                                                    dtype = str)
                        Open_origin.close()
                    
                    else:
                        Data_origins = pd.DataFrame(columns = [u'婚博会id'])
                        Data_sheetnames = pd.ExcelFile(Dir_origin).sheet_names
                        for Datasheetname in Data_sheetnames:
                            Data_origin = pd.read_excel(Dir_origin,
                                                        sheetname = Datasheetname,
                                                        keep_default_na = False,
                                                        dtype = str,
                                                         )
                            
                            if len(Data_origin) != 0 and len(Data_sheetnames) > 1:
                                Data_origins = Data_origins.append(Data_origin)
                            else:
                                Data_origins = Data_origin
                    
                    Data_result = Data_result.append(Data_origins)
                    Data_result.reset_index(inplace = True)
                #print(u'【',self.File_name,u'】文件夹数据读取完毕',sep = '')
            else:
                print(u'【',self.File_name,u'】文件夹不存在文件',sep = '')
            
        except Exception as e:
            print(e)
            print(u'【',self.File_name,u'】文件夹数据读取失败',sep = '')
            
        return(Data_result)

#D = File_Read_Traversal(u'Separated').Origin_Read()
#if __name__ == '__main__':
#    File_Read()

#Data_original = File_Read().Original_Read()
#Data_priority = File_Read().Priority_Read()
#Data_huifang = File_Read().Huifang_Read()

