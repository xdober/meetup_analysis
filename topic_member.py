import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

# group_member_info=pd.read_csv(Const.MEMBER_PATH, encoding="iso-8859-1")
# # member_info=pd.read_csv(Const.REAL_MEMBER_PATH, encoding="iso-8859-1")
# topic_member_info=pd.read_csv(Const.MMB_TPC_PATH, encoding="iso-8859-1")
#
# # 分析每个member加入的group和topic的关系
# groups_per_member = group_member_info.groupby(['member_id']).size()
# grp_mem_df=pd.DataFrame({'member_id':groups_per_member.index,'groups':groups_per_member.values})
# # df1 = pd.DataFrame({"count1":group_member_info.groupby([group_member_info['member_id'], group_member_info['city']]).size()})
# topics_per_member=topic_member_info.groupby(['member_id']).size()
# tpc_mem_df=pd.DataFrame({'member_id':topics_per_member.index,'topics':topics_per_member.values})
# tpc_mem_df=pd.merge(grp_mem_df,tpc_mem_df).sort_values('groups',ascending=False)
# rd.to_csv_noindex(tpc_mem_df,'result/topic and group number per member.csv')
# print(tpc_mem_df)

def newRead():
    tgm_info=pd.read_csv('result/topic and group number per member.csv')
    mem_df=pd.read_csv(Const.REAL_MEMBER_PATH)
    # print(tgm_info.sort_values(['topics','groups'],ascending=False))
    ave=tgm_info.groupby('topics').size().reset_index(name='members_count')
    print(ave)

def onlyTopicMember():
    topic_member_info = pd.read_csv(Const.MMB_TPC_PATH, encoding="iso-8859-1")
    topics_per_member=topic_member_info.groupby(['member_id']).size()
    tpc_mem_df=pd.DataFrame({'member_id':topics_per_member.index,'topics':topics_per_member.values})
    print(tpc_mem_df.groupby('topics').size().reset_index(name='members_count'))
    tpc_mem_df=tpc_mem_df.groupby('topics').size().reset_index(name='members_count')
    rd.to_csv_noindex(tpc_mem_df,'result/members follow how many topics.csv')

onlyTopicMember()
