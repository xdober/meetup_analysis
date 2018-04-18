import pandas as pd
import read_tools as rd
from constant import Const

# 保存真正的members
def saveRealMembers():
    memberGroup=pd.read_csv(Const.MEMBER_PATH, encoding="iso-8859-1")[['member_id', 'city', 'state', 'hometown', 'member_name']]
    mem_info=memberGroup.drop_duplicates()
    mem_info=mem_info.replace([r'(.*)[C|c]hicago(.*)', r'(.*)[S|s]an [F|f]rancisco(.*)', r'(.*)[N|n]ew [Y|y]ork(.*)'],['Chicago Area','San Francisco Area','New Youk Area'],regex=True)
    rd.to_csv_noindex(mem_info,'data/members_no_dump.csv')
def testMember():
    mem_info=pd.read_csv('data/members_no_dump.csv')
    # mem_info=mem_info.replace([r'(.*)[C|c]hicago(.*)', r'(.*)[S|s]an [F|f]rancisco(.*)', r'(.*)[N|n]ew [Y|y]ork(.*)'],['Chicago Area','San Francisco Area','New Youk Area'],regex=True)
    groupedby=mem_info.groupby('city')
    print(groupedby.size())

# 把一个member的群组按照category分类，并返回Series序列
def gbgbcate(df):
    nGB=rd.info_split_merge(df,'city_y')
    nGB.name=df['member_id'].values[0]
    # 只保留了前10项数量较多的category
    nGB=pd.DataFrame({'member_id':nGB.name,'category':nGB.index,'counts':nGB.values}).head(10)
    nGB=nGB.set_index('member_id',append=True).swaplevel(0,1)
    return nGB
# 把member按照city分类，统计加入的group所属的类别
def oneCityDeal(info,group):
    mem_grp=pd.merge(info[['member_id','city','group_id']],group[['group_id','category.shortname','city']],on='group_id')
    # print(mem_grp)
    gb_mem=mem_grp.groupby('member_id')
    gb = [gb_mem.get_group(x) for x in gb_mem.groups]
    for x in range(0,len(gb)):
        gb[x]=gbgbcate(gb[x])
        print(gb[x])
    gb=pd.concat(gb)
    gb.index.names=['member_id','No.']
    print(gb)
    return gb

def memberGroup():
    mem_grp_info=pd.read_csv(Const.MEMBER_PATH, encoding="iso-8859-1")
    mem_grp_chicago=mem_grp_info.loc[mem_grp_info.iloc[:,2].str.contains(r'(.*)[C|c]hicago(.*)')]
    # mem_grp_nyk=mem_grp_info[mem_grp_info['city']=='New York']
    # mem_grp_sf=mem_grp_info[mem_grp_info['city']=='San Francisco']
    group_info=pd.read_csv(Const.GROUP_PATH)
    oneCityDeal(mem_grp_chicago,group_info)

# saveRealMembers()
# testMember()
memberGroup()