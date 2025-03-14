# 数据处理文件
# 将日用表相加，总的链接到档案明细表
# 再按每月投票预测
# 1. 先按月进行, 新增加12+10个月的数据到档案表中，22（月）* 3（高，平，低）

import pandas as pd
import numpy as np
from time import *
import time

def get_database(path='training_dataset'):
    dangan_path = path + '/train_dangan.csv'
    date_path = path + '/train_date.csv'
    month_path = path + '/test_month.csv'

    dangan_data = pd.read_csv(dangan_path,encoding = 'gbk')
    dangan_data = dangan_data.fillna(0)   # 空缺地方补充0
    dangan_data = dangan_data[['id','elec_type_name','volt_name','run_cap']]
    date_data = pd.read_csv(date_path,encoding = 'gbk')
    date_data = date_data.fillna(0)
    month_data = pd.read_csv(month_path,encoding = 'gbk')
    month_data = month_data.fillna(0)

    # 处理档案时间
    # times_1970 = time.mktime(time.strptime("1971-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))
    # build_time = dangan_data['BUILD_DATE'].values.tolist()  # 变成list
    # change_type_time = []
    # # 转换成int,并扩充到9位
    # for item in build_time:
    #     times = item.split(' ')[0].split('/')
    #     for i in range(9):
    #         if i < len(times):
    #             times[i] = int(times[i])
    #         else:
    #             times.append(0)
    #     time_now = int(time.mktime(tuple(times)))  # 绝对时间
    #     t = int((time_now - times_1970) / 60 / 60 / 24 / 30)
    #     change_type_time.append(t)
    # dangan_data['BUILD_DATE'] = change_type_time
    # print(dangan_data.dtypes)

    # 处理月份，合并数据
    # 添加新列，22月*3
    new_month_feature = []   # 为新生成的列取名
    for i in range(1,23):
        new_month_feature.append(str(i)+'_pq_f')
        new_month_feature.append(str(i)+'_pq_g')
        new_month_feature.append(str(i)+'_pq_p')

    month_data = month_data[['id','ym','pq_f','pq_g','pq_p']]

    month_data["pq_f"] = month_data["pq_f"].astype("str")
    month_data["pq_g"] = month_data["pq_g"].astype("str")
    month_data["pq_p"] = month_data["pq_p"].astype("str")

    month_data['m'] = month_data['pq_f'] + '*' + month_data['pq_g'] + '*' + month_data['pq_p']
    dd = month_data.groupby('id')['m'].agg('*'.join)
    dd = pd.DataFrame(data=dd)
    dd = dd['m'].str.split('*', expand=True)
    dd.columns = new_month_feature
    # 将档案和月细节拼接
    month_dangan = dd.merge(dangan_data, how='left', on='id')
    month_dangan.to_csv(path +'/Result.csv',index=0)  # 不保存行索引

    return month_dangan

# 对date求标准差
def get_date(path='training_dataset'):
    date_path = path + '/train_date.csv'
    anl_path = path + '/Result2.csv'
    date_data = pd.read_csv(date_path,encoding = 'gb2312')
    anl_data = pd.read_csv(anl_path)
    date_data = date_data.fillna(0)

    dd = date_data.groupby('ID')['kwh'].std()
    dd = pd.DataFrame(data=dd)
    print(dd)
    # 将日细节拼接
    result = dd.merge(anl_data, how='left', on='ID')
    result.to_csv(path + '/Result_date.csv', index=0)  # 保存行索引

def nomalize(a,b,c):
    return (max(a,max(b,c))-min(a,min(b,c))) / (min(a,min(b,c))+ 10)

# 对每个月进行处理
def get_month(path):
    month_path = path + '/test_month.csv'
    month_data = pd.read_csv(month_path, encoding='gb2312')
    month_data['fangchaValue'] = month_data.apply(lambda x: nomalize(x['pq_f'], x['pq_g'], x['pq_p']), axis=1)
    print(month_data)

    month_data.to_csv(path + '/month2.csv', index=0)

def get_database2(path):
    dangan_path = path + '/train_dangan.csv'
    month_path = path + '/month2.csv'

    dangan_data = pd.read_csv(dangan_path, encoding='gbk')
    dangan_data = dangan_data.fillna(0)  # 空缺地方补充0
    dangan_data = dangan_data[['id', 'elec_type_name', 'volt_name', 'run_cap']]
    month_data = pd.read_csv(month_path, encoding='gbk')
    month_data = month_data.fillna(0)

    # 处理档案时间
    # times_1970 = time.mktime(time.strptime("1971-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))
    # build_time = dangan_data['BUILD_DATE'].values.tolist()  # 变成list
    # change_type_time = []
    # # 转换成int,并扩充到9位
    # for item in build_time:
    #     times = item.split(' ')[0].split('/')
    #     for i in range(9):
    #         if i < len(times):
    #             times[i] = int(times[i])
    #         else:
    #             times.append(0)
    #     time_now = int(time.mktime(tuple(times)))  # 绝对时间
    #     t = int((time_now - times_1970) / 60 / 60 / 24 / 30)
    #     change_type_time.append(t)
    # dangan_data['BUILD_DATE'] = change_type_time
    # print(dangan_data.dtypes)

    # 处理月份，合并数据
    # 添加新列，22月
    new_month_feature = []  # 为新生成的列取名
    for i in range(1, 23):
        new_month_feature.append(str(i) + '_nomal')

    month_data['m'] = month_data['fangchaValue'].astype("str")
    dd = month_data.groupby('id')['m'].agg('*'.join)
    dd = pd.DataFrame(data=dd)
    dd = dd['m'].str.split('*', expand=True)
    dd.columns = new_month_feature
    print(dd)
    # 将档案和月细节拼接
    month_dangan = dd.merge(dangan_data, how='left', on='id')
    month_dangan.to_csv(path + '/Result_month.csv', index=0)  # 保存行索引



def get_fangcha(path):
    month_path = path + '/Result.csv'
    month_nomal_path = path +'/Result_month.csv'
    month_data = pd.read_csv(month_path, encoding='gbk')
    month_nomal = pd.read_csv(month_nomal_path, encoding='gbk')
    month_data['fangcha'] = month_data.iloc[:,11:77].std(axis=1)
    month_data['jiaquan'] = month_data['fangcha']*0.3+month_data.iloc[:,11:77].mean(axis=1)*0.7
    dd = month_data[['id','fangcha','jiaquan']]
    month_dangan = dd.merge(month_nomal, how='left', on='id')
    month_dangan.to_csv(path + '/Result_dangan.csv', index=0)  # 保存行索引

if __name__ == '__main__':
    get_fangcha('B_testdataset')