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

class Group():
    def __init__(self,ID):
        self.id=ID
        self.members=0
        self.records=None
        self.start=pd.to_datetime('20000101')
        self.end=pd.to_datetime('20000101')
        self.trendsSer=None
# 统计在某个时间点之前的数量
def beforeTime(df,tm,dur):
    delta=pd.to_datetime('20110201')-pd.to_datetime('20110101')
    ndf=df[df['joined']<tm]
    if dur:
        ndf=ndf[(tm-ndf['joined'])<delta]
    return len(ndf)
# group中member随时间的变化
# df:group_id相同的member_join_group数据
def memberTrendsOneGroup(df,dur=False):
    num_ser=[]
    start_time=df['joined'].min()
    end_time=df['joined'].max()
    now=df['joined'].min()
    gap=pd.to_datetime('20110102')-pd.to_datetime('20110101')
    while (now<=end_time):
        num=beforeTime(df,now,dur)
        num_ser.append(num)
        now=now+gap
    num_ser=pd.Series(data=num_ser,index=pd.date_range(start_time,periods=len(num_ser)))
    # print(num_ser)
    # plt.plot(num_ser)
    # plt.show()
    return num_ser
# 自定义排序函数
def customSortKey(df):
    start=df['joined'].min()
    return start
def groupMemberTrends():
    mem_join_group=pd.read_csv(Const.MEMBER_PATH, encoding="iso-8859-1")[['member_id','joined','visited','group_id']]
    group_info=pd.read_csv(Const.GROUP_PATH)[['group_id','members']].set_index('group_id')
    mem_join_group['joined']=pd.to_datetime(mem_join_group['joined'])
    mem_join_group['visited']=pd.to_datetime(mem_join_group['visited'])
    gb=mem_join_group.groupby('group_id')
    gb=[gb.get_group(x) for x in gb.groups]
    gb=[item for item in gb if len(item)>100 and len(item)*1.0/(group_info['members'][item['group_id'].values[0]])>0.99]
    print(len(gb))
    gb.sort(key=lambda x: customSortKey(x))
    num_sers=[]
    for i in range(0,len(gb)):
        num_sers.append(memberTrendsOneGroup(gb[i]))

        plt.plot(num_sers[i])
    print(num_sers[4])
    print(num_sers[4].index)
    # print(len(gb[800]))
    # memberTrendsOneGroup(gb[500])
    plt.show()

# 选择需要选取的member，因为member数量太多，这里只选了加入群组数量排名前20的member(先按照city分为三类，每一类选20个)
def selectMember(MEM_GRP_PATH):
    member_group_df = pd.read_csv(MEM_GRP_PATH, encoding="iso-8859-1")[['member_id', 'joined', 'visited', 'group_id']]
    members=member_group_df.groupby('member_id').size().sort_values(ascending=False)
    member_ids=members.index[0:20]
    member_group_df = member_group_df[member_group_df['member_id'].isin(member_ids)]
    rd.to_csv_noindex(member_group_df,MEM_GRP_PATH.split('.')[0]+'_top20.csv')
def memberGroupTrends():
    mem_join_group=pd.read_csv(Const.MEMBER_PATH.split('.')[0]+'_top20.csv', encoding="iso-8859-1")[['member_id','joined','visited','group_id']]
    mem_join_group['joined']=pd.to_datetime(mem_join_group['joined'])
    mem_join_group['visited']=pd.to_datetime(mem_join_group['visited'])
    gb=mem_join_group.groupby('member_id')
    # memGRPs=gb.size()
    # print(type(memGRPs))
    # print(memGRPs)
    # memGRPs=memGRPs[memGRPs>400]
    # memGRPs=memGRPs.sort_values(ascending=False)
    # print(memGRPs)
    gb=[gb.get_group(x) for x in gb.groups]
    gb.sort(key=lambda x: customSortKey(x))
    # gb.sort(key=len,reverse=True)
    num_sers=[]
    for i in range(0,len(gb)):
        num_sers.append(memberTrendsOneGroup(gb[i],True))

        plt.plot(num_sers[i])
    plt.show()


# dealGroup()
# groupCreatedMembers()
# groupMemberTrends()
# selectMember(Const.MEMBER_PATH)
memberGroupTrends()