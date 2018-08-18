# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 22:20:42 2017

@author: cwl
"""

import os
import time
import pandas as pd
#import Fotmat_ChangeExcel

class File_Save_First(object):
    """文件存储"""
    def __init__(self,Data_result):
        Dir = os.getcwd()
        self.Dir_result = Dir + os.sep + u'结果_一遍数据源'
        self.Dir_availability = Dir + os.sep + u'结果_余量'
        self.Dir_backflow = Dir + os.sep + u'结果_回流检查'
        
        self.Data_result = Data_result
        #self.Data_recycle_result = Data_recycle_result
        
    def Summary_Deal(self):
        ##汇总
        self.Critical_save(self.Dir_result)
        self.Critical_save(self.Dir_availability)
        self.Critical_save(self.Dir_backflow)
        
        Index_availability = self.Result_save(self.Data_result)
        self.Availability_Save(self.Data_result.loc[Index_availability,[u'分配天数',u'一次电话内容']])
        #self.Backflow_Save(self.Dir_backflow,self.Data_recycle_result)
        
    def Critical_save(self,Dir):
        ##保存文件路径判定##
        if os.path.exists(Dir):
            
            pass
        else:
            os.mkdir(Dir)

    def Result_save(self,Data_result):
        ##保存一遍数据源##
        Dir_resultdistribution = self.Dir_result + os.sep + \
                                      u'数据源_一遍-' + \
                                      time.strftime('%Y%m%d_%H%M',time.localtime()) + \
                                      '.xlsx'
        
        try:
            print(u'一遍数据源正在保存....')            
            Index_availability = Data_result[Data_result[u'Sparated_reason'] == ''].index
            Data_availability = Data_result.loc[Index_availability]
            Index_noavailability = Data_result[Data_result[u'Sparated_reason'] != ''].index
            Data_noavailability = Data_result.loc[Index_noavailability]            
            
            try:
                del Data_availability[u'Sparated_reason']
            except:
                pass
            
            Writer_result = pd.ExcelWriter(Dir_resultdistribution)
            for Data_item,Data_name in [(Data_availability,u'数据源_一遍_正常'),
                                        (Data_noavailability,u'数据源_一遍_Separated')]:
                Data_item.to_excel(Writer_result,
                                   sheet_name = Data_name,
                                   encoding = 'gb18030',
                                   index = False)
            
            Writer_result.save()
            print(u'一遍数据源保存完毕')
            return(Index_availability)
        
        except:
            print(u'一遍数据源保存失败,10秒后退出')
            time.sleep(10)
            exit()

    def Availability_Save(self,Data_availability):
        ##余量表##
        try:
            print(u'正在保存余量表....')
            Dir_availability = self.Dir_availability + os.sep + \
                                      u'余量_一遍-' + \
                                      time.strftime('%Y%m%d_%H%M',time.localtime()) + \
                                      '.xlsx'

            Data_hbh = Data_availability[~(Data_availability[u'一次电话内容'].str.startswith(u'家博会')) &
                                         ~(Data_availability[u'一次电话内容'].str.startswith(u'儿博会'))]

            Data_jbh = Data_availability[(Data_availability[u'一次电话内容'].str.contains(u'家博会')) &\
                                         ~(Data_availability[u'一次电话内容'].str.contains(u'婚博会|儿博会'))]
            Data_ebh = Data_availability[(Data_availability[u'一次电话内容'].str.contains(u'儿博会')) &\
                                         ~(Data_availability[u'一次电话内容'].str.contains(u'婚博会'))]
            
            Writer_availability = pd.ExcelWriter(Dir_availability)
            for Data_item,Name_item in [(Data_availability,u'总'),
                                        (Data_hbh,u'婚博会'),
                                        (Data_jbh,u'家博会'),
                                        (Data_ebh,u'儿博会')]:
                try:
                    Pivot_data = pd.pivot_table(Data_item[[u'分配天数',u'一次电话内容']],
                                                           index = u'一次电话内容',
                                                           columns = u'分配天数',
                                                           aggfunc = len,
                                                           margins = True,
                                                           margins_name = u'汇总')                
                    Pivot_data.reset_index(inplace = True)
                    
                    Replace_columns = [('0',0),('1',1),('2',2),('3',3)]
                    for Replace_column in Replace_columns:
                        if Replace_column[0] in Pivot_data.columns:
                            Pivot_data.rename(columns = {Replace_column[0]:Replace_column[1]},inplace = True)
                    
                    Pivot_data.to_excel(Writer_availability,
                                        sheet_name = Name_item,
                                        encoding = 'gb18030',
                                        index = False)
                    
                    worksheet = Writer_availability.sheets[Name_item]
                    workbook = Writer_availability.book
                    worksheet.freeze_panes(1, 0)
                    
                    Header_format = workbook.add_format({'bold':True,#粗体
                                                         'text_wrap':'True',#自动换行
                                                         'align':'center',#平行对齐
                                                         'valign':'vcenter',#垂直对齐
                                                         'font_name':u'黑体',
                                                         'font_size':'11',
                                                         'fg_color':'#778899',
                                                         })

                    Conter_format_firstcolumn = workbook.add_format({'align':'center',#平行对齐
                                                                     'valign':'vcenter',#垂直对齐
                                                                     'font_name':u'微软雅黑',
                                                                     'font_size':'11',
                                                                     'bold':True,
                                                                     })
                    
                    Conter_format = workbook.add_format({'align':'center',#平行对齐
                                                         'valign':'vcenter',#垂直对齐
                                                         'font_name':u'微软雅黑',
                                                         'font_size':'11',
                                                         })

                    for col_num,value in enumerate(Pivot_data.columns.values):
                        worksheet.write(0,col_num,value,Header_format)
                    
                    worksheet.set_row(0,17.25)
                    worksheet.set_column('A:A',56,cell_format = Conter_format_firstcolumn)
                    worksheet.set_column('B:G',10.88,cell_format = Conter_format)
                
                except Exception as e:
                    print(e)
            
            Writer_availability.save()
            print(u'余量表保存完毕')
        except:
            print(u'余量表保存失败,即将退出')
            exit()

    def Backflow_Save(self,Data_recycle_result):
        try:
            print(u'回流检查结果正在保存....')
            Dir_backflow = self.Dir_backflow + os.sep + u'回流检查-' + time.strftime('%Y%m%d_%H%M',time.localtime()) + '.xlsx'
            Writer_backflow = pd.ExcelWriter(Dir_backflow)
            Data_recycle_result.to_excel(Writer_backflow,encoding = 'gb18030',index = False,sheet_name = u'回流检查')
            worksheet =Writer_backflow.sheets[u'回流检查']
            workbook = Writer_backflow.book
            worksheet.freeze_panes(1,0)
            Header_format = workbook.add_format({'bold':True,#粗体
                                                 'text_wrap':'True',#自动换行
                                                 'align':'center',#平行对齐
                                                 'valign':'vcenter',#垂直对齐
                                                 })            
                    
            for col_num,value in enumerate(Data_recycle_result.columns.values):
                worksheet.write(0,col_num,value,Header_format)
            
            Writer_backflow.save()
            print(u'回流检查结果保存完毕')
        except Exception as e:
            print(u'回流检查结果保存失败')
            print(e)
