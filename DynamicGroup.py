import pandas as pd
import read_tools as rd
import numpy as np
from constant import Const
from pylab import *

# 按照category将group分组
def SplitGroup(group_info):
    groupGB=group_info.groupby('category.name')
    groups_per_cate=[groupGB.grt_group(x) for x in groupGB.groups]
    groups_per_cate=groups_per_cate.sort(key=len,reverse=True)
    return groups_per_cate
def timeNumber(info,**kw):
    by = 'created'
    if 'created' in kw:
        by = kw[by]
    gapp = info[by].dt.year
    if 'gap' in kw:
        if kw['gap'] == 'month':
            gapp = [info[by].dt.year, info[by].dt.month]
    info_created = info[by].groupby(gapp).count()
    # print(gapp[0])
    return info_created
# 统计每个时间段内群组的数量（包括新建的群组和截至某一时刻全部的群组）
def timeNumSer(info,sample='M'):
    info.set_index(info['simple_date'], inplace=True)
    group_resample = info.resample(sample)
    preSer = group_resample.count()
    new_group_series = pd.Series(data=preSer['city'].values, index=preSer.index)
    new_group_series.name = 'counts'
    group_series=new_group_series.copy()
    for x in range(1,len(group_series),1):
        group_series[x]=group_series[x-1]+group_series[x]
    return [new_group_series,group_series]
def dealGroup():
    group_info=pd.read_csv(Const.GROUP_PATH)[['group_id', 'category.shortname', 'city_id', 'city', 'created', 'members']]
    group_info['created']=pd.to_datetime(group_info['created'])
    group_info['simple_date']=group_info['created'].apply(lambda df : pd.datetime(year=df.year, month=df.month, day=df.day))
    group_series=timeNumSer(group_info,sample='M')
    print(group_series[0])
    # plt.plot(group_series[0])
    plt.plot(group_series[1])
    plt.show()

# group创建时间与member数量的走势
def groupCreatedMembers():
    group_info=pd.read_csv(Const.GROUP_PATH)[['group_id', 'category.shortname', 'city', 'created', 'members', 'rating']]
    group_info=group_info[group_info['members']>10000]
    group_info=group_info.sort_values(['members','group_id'])
    # group_info['created']=pd.to_datetime(group_info['created'])
    # group_info.set_index(group_info['created'],inplace=True)
    print(group_info.head(20))
    print(len(group_info))

# 统计在某个时间点之前的数量
def beforeTime(df,tm):
    ndf=df[df['joined']<tm]
    return len(ndf)
# group中member随时间的变化
# df:group_id相同的member_join_group数据
def memberTrendsOneGroup(df):
    num_ser=[]
    start_time=df['joined'].min()
    end_time=df['joined'].max()
    now=df['joined'].min()
    gap=pd.to_datetime('20110105')-pd.to_datetime('20110101')
    while (now<=end_time):
        num=beforeTime(df,now)
        num_ser.append(num)
        now=now+gap
    num_ser=pd.Series(data=num_ser,index=pd.date_range(start_time,periods=len(num_ser)))
    # print(num_ser)
    # plt.plot(num_ser)
    # plt.show()
    return num_ser
def customSortKey(df):
    start=df['joined'].min()
    return start
def groupMemberTrends():
    mem_join_group_chi=pd.read_csv(Const.MEM_GRP_CHI)
    mem_join_group_ny=pd.read_csv(Const.MEM_GRP_NY)
    mem_join_group_sf=pd.read_csv(Const.MEM_GRP_SF)
    print(mem_join_group_chi.head())
    print(mem_join_group_ny.head())
    print(mem_join_group_sf.head())
    mem_join_group=pd.concat([mem_join_group_chi,mem_join_group_ny,mem_join_group_sf])
    group_info=pd.read_csv(Const.GROUP_PATH)[['group_id','members']]
    mem_join_group_chi['joined']=pd.to_datetime(mem_join_group['joined'])
    gb=mem_join_group_chi.groupby('group_id')
    gb=[gb.get_group(x) for x in gb.groups]
    gb=[item for item in gb if len(item)>2000]
    print(len(gb))
    gb.sort(key=lambda x: customSortKey(x))
    num_sers=[]
    for i in range(0,10):
        num_sers.append(memberTrendsOneGroup(gb[i]))
        plt.plot(num_sers[i])
    # print(len(gb[800]))
    # memberTrendsOneGroup(gb[500])
    plt.show()

# dealGroup()
# groupCreatedMembers()
groupMemberTrends()