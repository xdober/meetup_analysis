import pandas as pd
import read_tools as rd
import numpy as np
from constant import Const
from pylab import *

# 把event信息按照group分组
def event_per_group(event_info):
    event_gb=event_info.groupby(['group_id'])
    events_per_group=[event_gb.get_group(x) for x in event_gb.groups]
    events_per_group.sort(key=len,reverse=True)
    print(events_per_group[30])
    return events_per_group

# 统计在某个时间点之前的数量
def beforeTime(df,tm,created):
    delta=pd.to_datetime('20110201')-pd.to_datetime('20110101')
    ndf=df[df[created]<tm]
    ndf=ndf[ndf[created]>tm-delta]
    return len(ndf)/30
# group中member随时间的变化
# df:group_id相同的member_join_group数据
def memberTrendsOneGroup(df,created='created'):
    num_ser=[]
    start_time=df[created].min()
    end_time=df[created].max()
    now=df[created].min()
    gap=pd.to_datetime('20110102')-pd.to_datetime('20110101')
    while (now<=end_time):
        num=beforeTime(df,now,created)
        num_ser.append(num)
        now=now+gap
    num_ser=pd.Series(data=num_ser,index=pd.date_range(start_time,periods=len(num_ser)))
    return num_ser

# 处理event信息
def dealEvents():
    event_info=pd.read_csv(Const.EVENT_PATH)
    event_info['created']=pd.to_datetime(event_info['created'])
    event_info['event_time']=pd.to_datetime(event_info['event_time'])
    event_info['updated']=pd.to_datetime(event_info['updated'])
    # events_per_group = event_per_group(event_info)
    # event_created_fig = rd.info_groupedby_created(events_per_group[0], gap='month', notsave='yes', created='created')
    # event_start_fig = rd.info_groupedby_created(events_per_group[0], gap='month', notsave='yes', created='event_time')
    Updated=memberTrendsOneGroup(event_info,'updated')
    Created=memberTrendsOneGroup(event_info)
    Start=memberTrendsOneGroup(event_info,'event_time')
    plt.plot(Created)
    plt.plot(Updated)
    plt.plot(Start)
    plt.show()

# 返回一个序列
def deltaTrends(df,by='created'):
    ser=pd.Series(data=df['dur'].values/np.timedelta64(1, 'D'),index=df[by])
    ser=ser.sort_index()
    sergb=ser.groupby(ser.values)

    # Min=pd.to_datetime(df[by].min().strftime('%Y%m%d'))
    # Max=pd.to_datetime(df[by].max().strftime('%Y%m%d'))
    # print(Min)
    minDelta=pd.to_datetime('20110201')-pd.to_datetime('20110201')
    maxDelta=df['dur'].max()
    tmp=minDelta
    delta=pd.to_datetime('20110208')-pd.to_datetime('20110101')
    deltas=[]
    while tmp<maxDelta:
        nextDelta=tmp+delta
        ndf=df[df['dur']>=tmp]
        ndf=ndf[ndf['dur']<nextDelta]
        deltas.append(len(ndf))
        tmp=nextDelta
    return deltas
# event 自创建到举行的时间差分析
def eventCreatToStart():
    event_info=pd.read_csv('data/event_simple.csv')
    event_info['created']=pd.to_datetime(event_info['created'])
    event_info['event_time']=pd.to_datetime(event_info['event_time'])
    event_info['updated']=pd.to_datetime(event_info['updated'])
    event_info['dur']=event_info['event_time']-event_info['created']
    print(event_info.head())
    dur_ser=deltaTrends(event_info)
    # print(dur_ser)
    plt.plot(dur_ser)
    plt.show()

# 简化event信息
def simplifyEvent():
    event_info=pd.read_csv(Const.EVENT_SIMP_PATH)[['event_id', 'created', 'duration', 'group_id', 'group.who', 'rsvp_limit', 'event_time', 'updated', 'utc_offset', 'venue.address_1', 'venue.city', 'venue_id', 'waitlist_count', 'yes_rsvp_count']]
    rd.to_csv_noindex(event_info,'data/event_simple.csv')

# simplifyEvent()
# dealEvents()
eventCreatToStart()