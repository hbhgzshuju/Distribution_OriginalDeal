# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 22:21:43 2017

@author: 中国婚博会_广州数据部

E-mail: 1813528779@qq.com

To: Sharing and gratitude are my attitude towards life
"""

import File_Read
import Select_Deal
import Nominal_Normal
import Nominal_Freedom
import DistributionDate_Deal
#import Match_Phone
#import Match_Loveid
import Stage_Deal
import Repetition_Deal
#import Recycle_Check
import Sparated_Reason
import Repetition_Phone_Deal
import File_Save
import datetime

#默认给当天余量,只对分配天数"2暂时不打"有影响

Time_now = datetime.datetime.now().strftime("%H:%M:%S")

if Time_now > '18:00:00':
    Date_give = (datetime.datetime.now() + datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
else:
    Date_give = datetime.datetime.now().strftime("%Y-%m-%d")


class Control(object):
    """控制文件"""
    def __init__(self):
        self.Data_original = File_Read.File_Read().Original_Read()
        #self.Data_original = Data_original
        self.Data_priority = File_Read.File_Read().Priority_Read()
        self.Data_freedom = File_Read.File_Read().Freedom_Read()
        self.Data_huifang = File_Read.File_Read_Traversal(u'ID_huifang').Origin_Read()
        self.Data_research_phone = File_Read.File_Read().Research_phone_Read()
        self.Data_research_loveid = File_Read.File_Read().Research_loveid_Read()
        self.Data_separated = File_Read.File_Read_Traversal(u'Separated').Origin_Read()
        self.Data_separated_reason = File_Read.File_Read_Traversal(u'Separated_Reason').Origin_Read()
                
    def Summary_Deal(self):
        ##汇总
        self.Control_Deal(self.Data_original,
                          self.Data_priority,
                          self.Data_freedom,
                          self.Data_huifang,
                          self.Data_research_phone,
                          self.Data_research_loveid,
                          self.Data_separated,
                          self.Data_separated_reason)
        
    def Control_Deal(self,Data_original,Data_priority,Data_freedom,Data_huifang,Data_research_phone,Data_research_loveid,Data_separated,Data_separated_reason):
        ##处理
        Columns_original = Data_original.columns.tolist() + [u'Sparated_reason']
        #print(u'正在根据婚博会id匹配调研项....')
        #Data_original = Match_Loveid.Match_Loveid(Data_original,Data_research_loveid).Summary_Deal()
        #print(u'调研项-婚博会id匹配成功')

        print(u'正在处理孕婴状态....')
        Data_original = Stage_Deal.Main(Data_original)
        #print(u'孕婴状态处理完毕')

        print(u'正在筛选一遍数据源....')
        Index_part1,Index_part2,Index_part3,Index_part4 = Select_Deal.Select_Deal(Data_original,Data_huifang).Summary_Deal()
        Index_all = Index_part1 + Index_part2 + Index_part3 + Index_part4
        #print(u'一遍数据源筛选完毕')
        
        print(u'正在处理电话分型....')
        Data_original.loc[Index_part1 + Index_part2,u'一次电话内容'] = Nominal_Normal.Nominal_Summary(Data_priority).Summary_Deal(Data_original.loc[Index_part1 + Index_part2])
        Data_original.loc[Index_part1 + Index_part2,u'一次电话内容'] = Nominal_Freedom.Nominal_Freedom(Data_original.loc[Index_part1 + Index_part2],Data_freedom) 
        Data_original.loc[Index_part3 + Index_part4,u'一次电话内容'] = Data_original.loc[Index_part3 + Index_part4,u'a一次电话内容'].values.tolist()
        
        Index_afuzhu = Data_original[(Data_original[u'a一次电话辅助'].str.contains(u'订单不一致')) &\
                                     (~(Data_original[u'一次电话内容'].str.contains(u'订单不一致')))].index
                                     
        Data_original.loc[Index_afuzhu,u'一次电话内容'] = Data_original.loc[Index_afuzhu,u'一次电话内容'] + u'-订单不一致'

        Index_afuzhu = Data_original[Data_original[u'a一次电话辅助'].str.contains(u'色色订单')].index
                                     
        #Data_original.loc[Index_afuzhu,u'一次电话内容'] = Data_original.loc[Index_afuzhu,u'一次电话内容'] + u'-色色订单'

        Index_afuzhu = Data_original[(Data_original[u'a一次电话辅助'].str.contains(u'大于10岁')) &\
                                     ~(Data_original[u'一次电话内容'].str.contains(u'婚博会|家博会'))].index
                                     
        Data_original.loc[Index_afuzhu,u'一次电话内容'] = Data_original.loc[Index_afuzhu,u'一次电话内容'] + u'-大于10岁'
        #print(u'电话分型处理成功')

        #try:
        #    print(u'正在检查回流....')
        #    Recycle_check = File_Read.File_Read_Traversal(u'Recycle_Check').Origin_Read()
        #    Data_original,Data_recycle_result = Recycle_Check.Recycle_Check(Data_original,Recycle_check).Recycle_Summary()
        #    print(u'回流检查完毕')
        #except Exception as e:
        #    print(u'回流检查失败,将不做回流处理')
        #    print(e)
        
        Data_result = Data_original.loc[Index_all,:]
        
        print(u'正在处理分配天数....')
        Data_result[u'分配天数'] = DistributionDate_Deal.DistributionDate_Deal(Data_result,Date_give).Summary_Deal()
        #print(u'分配天数处理完毕')
        
        #print(u'正在根据手机匹配调研项....')
        #Data_result = Match_Phone.Match_Phone(Data_result,Data_research_phone).Match_Summary()
        #print(u'调研项-手机匹配成功')
                
        print(u'正在处理重复号码....')
        Data_result = Repetition_Deal.Repetition_Deal(Data_result)
        #print(u'重复号码处理完毕')
        
        print(u'正在标记隔开原因数据....')
        #标记Sparated文件
        Data_result[u'Sparated_reason'] = Sparated_Reason.Operation_Freedom(Data_result,Data_separated_reason)        
        
        for column in [u'婚博会id',u'新郎手机',u'新娘手机']:
            Data_separated_item = Data_separated[column][Data_separated[column] != ''].astype(str)
            if len(Data_separated_item) != 0:
                for column_result in [u'婚博会id',u'新郎手机',u'新娘手机']:
                    if column_result in Data_result.columns.tolist():
                        Index_separated = Data_result[(Data_result[column_result].astype(str).isin(Data_separated_item))].index
                        Data_result.loc[Index_separated,u'Sparated_reason'] = Data_result.loc[Index_separated,u'Sparated_reason'] + u'Sparated文件+'
            else:
                pass
        
        if u'Recycle_Judge' in Data_result.columns.tolist():
            Index_backflow = Data_result[Data_result[u'Recycle_Judge'].str.contains(u'异常')].index
            Data_result.loc[Index_backflow,u'Sparated_reason'] = Data_result.loc[Index_backflow,u'Sparated_reason'] + u'回流异常+'
        
        #标记非异常重复号码
        Repetition_phone = Repetition_Phone_Deal.Phone_Value_Counts(Data_original)
        Index_repetition = Data_result[(Data_result[u'新郎手机'].isin(Repetition_phone)) |
                                        (Data_result[u'新娘手机'].isin(Repetition_phone))].index
        
        Data_result.loc[Index_repetition,u'Sparated_reason'] = Data_result.loc[Index_repetition,u'Sparated_reason'] + u'号码重复+'
        
        Data_result[u'Sparated_reason'] = Data_result[u'Sparated_reason'].replace('\+$','',regex = True)
        print(u'隔开原因标记完毕')
        
        try:
            Data_result[u'办婚礼地'].replace([u'广州',u'非广州',u'佛山',u'非广州or佛山'],[u'本地',u'非本地',u'非本地',u'非本地'],inplace = True)
            print(u'【办婚礼地】:',Data_result[u'办婚礼地'].drop_duplicates().values.tolist())
        except:
            pass
        
        #Index_not_402 = Data_result[~(Data_result[u'签单'].str.contains(u'402'))&
        #                            ~(Data_result[u'一次电话内容'].str.contains(u'升级|订单'))].index
                                    
        #Data_result = Data_result.loc[Index_not_402]
        
        Data_result = Data_result[Columns_original]
        File_Save.File_Save_First(Data_result).Summary_Deal()

        #try:
        #    File_Save.File_Save_First(Data_result).Backflow_Save(Data_recycle_result)
        #except:
        #    pass

def Main():
    print(__doc__)
    Time_start = datetime.datetime.now()
    Control().Summary_Deal()
    Time_end = datetime.datetime.now()
    print(u'Spend_Time:',str(Time_end - Time_start),sep = '')

if __name__ == '__main__':
    Main()


