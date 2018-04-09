import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

# group_member_info=pd.read_csv(Const.MEMBER_PATH, encoding="iso-8859-1")
# # member_info=pd.read_csv(Const.REAL_MEMBER_PATH, encoding="iso-8859-1")
# topic_member_info=pd.read_csv(Const.MMB_TPC_PATH, encoding="iso-8859-1")
#
# # 分析每个member加入的group和topic的关系(仅数量上)
# groups_per_member = group_member_info.groupby(['member_id']).size()
# grp_mem_df=pd.DataFrame({'member_id':groups_per_member.index,'groups':groups_per_member.values})
# topics_per_member=topic_member_info.groupby(['member_id']).size()
# tpc_mem_df=pd.DataFrame({'member_id':topics_per_member.index,'topics':topics_per_member.values})
# tpc_mem_df=pd.merge(grp_mem_df,tpc_mem_df).sort_values('groups',ascending=False)
# # rd.to_csv_noindex(tpc_mem_df,'result/topic and group number per member.csv')
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
    # rd.to_csv_noindex(tpc_mem_df,'result/members follow how many topics.csv')

# 把一个maintopic下的群组按照category分类，并返回Series序列
def gbgbcate(df):
    nGB=rd.info_split_merge(df,'category.shortname')
    nGB.name=df['member_id'].values[0]
    nGB=pd.DataFrame({'member_id':nGB.name,'category':nGB.index,'counts':nGB.values})
    nGB=nGB.set_index('member_id',append=True).swaplevel(0,1)
    return nGB
def dealGroupsCategoryPerMember():
    member_group_df=pd.read_csv(Const.MEM_JOIN_GRP_TINY)
    group_cate_df=pd.read_csv(Const.GROUP_PATH, encoding="iso-8859-1")[['group_id','category.shortname']]
    member_category_df=pd.merge(member_group_df,group_cate_df)
    groupsPerMemberGB=member_category_df.groupby('member_id')
    print(groupsPerMemberGB.size())
    gb=[groupsPerMemberGB.get_group(x) for x in groupsPerMemberGB.groups]
    for x in range(0,len(gb)):
        gb[x]=gbgbcate(gb[x])
        print(gb[x])

def tinyDeal():
    member_group_df = pd.read_csv('data/tiny_member_group.csv', encoding="iso-8859-1")
    group_cate_df = pd.read_csv(Const.GROUP_PATH, encoding="iso-8859-1")[['group_id', 'category.shortname']]
    member_category_df = pd.merge(member_group_df, group_cate_df)
    groupsPerMemberGB = member_category_df.groupby('member_id')
    print(groupsPerMemberGB)
    gb = [groupsPerMemberGB.get_group(x) for x in groupsPerMemberGB.groups]
    for x in range(0, len(gb)):
        gb[x] = gbgbcate(gb[x])
        print(gb[x])

def selectMember():
    member_group_df = pd.read_csv(Const.MEMBER_PATH, encoding="iso-8859-1")[['member_id', 'group_id']]
    selSrc=pd.read_csv(Const.TPC_GRP_NUM_MEM)
    member_ids=selSrc['member_id'].head(20).values
    member_group_df = member_group_df[member_group_df['member_id'].isin(member_ids)]
    rd.to_csv_noindex(member_group_df,Const.MEM_JOIN_GRP_TINY)
    print(member_group_df)

# tinyDeal()
# selectMember()
dealGroupsCategoryPerMember()