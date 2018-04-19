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
    nGB=rd.info_split_merge(df,'category.shortname')
    nGB.name=df['member_id'].values[0]
    allCategorys=pd.read_csv(Const.CTGY_PATH)['category.shortname'].values
    nowCategorys=nGB.index
    ret_list = list(set(allCategorys) ^ set(nowCategorys))
    for cate in ret_list:
        nGB[cate]=0
    nGB=nGB.sort_index()
    # 只保留了前10项数量较多的category
    # nGB=pd.DataFrame({'member_id':nGB.name,'category':nGB.index,'counts':nGB.values}).head(10)
    # 保留全部category
    nGB=pd.DataFrame({'member_id':nGB.name,'category':nGB.index,'counts':nGB.values})
    nGB=nGB.set_index('member_id',append=True).swaplevel(0,1)
    return nGB
# 把member按照city分类，统计加入的group所属的类别
def oneCityDeal(info,group):
    mem_grp=pd.merge(info[['member_id','group_id']],group[['group_id','category.shortname','city']],on='group_id')
    # print(mem_grp)
    gb_mem=mem_grp.groupby('member_id')
    gb = [gb_mem.get_group(x) for x in gb_mem.groups]
    for x in range(0,len(gb)):
        gb[x]=gbgbcate(gb[x])
        # print(gb[x])
    gb=pd.concat(gb)
    gb.index.names=['member_id','No.']
    print(gb)
    # 保存到excel
    writer=pd.ExcelWriter('result/group_counts_percate_per_member_'+info.name+'.xlsx',engine='xlsxwriter')
    gb.to_excel(writer)
    writer.save()
    return gb
# 选择需要选取的member，因为member数量太多，这里只选了加入群组数量排名前20的member(先按照city分为三类，每一类选20个)
def selectMember(MEM_GRP_PATH):
    member_group_df = pd.read_csv(MEM_GRP_PATH, encoding="iso-8859-1")[['member_id', 'group_id']]
    members=member_group_df.groupby('member_id').size().sort_values(ascending=False)
    member_ids=members.index[0:20]
    member_group_df = member_group_df[member_group_df['member_id'].isin(member_ids)]
    rd.to_csv_noindex(member_group_df,MEM_GRP_PATH.split('.')[0]+'_top20.csv')
def selTop20():
    selectMember(Const.MEM_GRP_CHI)
    selectMember(Const.MEM_GRP_NY)
    selectMember(Const.MEM_GRP_SF)

# 把三个城市前20名member的统计信息保存起来（加入每一类别的群组数量）
def memberGroup():
    mem_grp_ny=pd.read_csv(Const.MEM_GRP_NY.split('.')[0]+'_top20.csv')
    mem_grp_chi=pd.read_csv(Const.MEM_GRP_CHI.split('.')[0]+'_top20.csv')
    mem_grp_sf=pd.read_csv(Const.MEM_GRP_SF.split('.')[0]+'_top20.csv')
    mem_grp_ny.name='new_york'
    mem_grp_chi.name='chicago'
    mem_grp_sf.name='san_francisco'
    group_info=pd.read_csv(Const.GROUP_PATH)
    ny=oneCityDeal(mem_grp_ny,group_info)
    chi=oneCityDeal(mem_grp_chi,group_info)
    sf=oneCityDeal(mem_grp_sf,group_info)

# 把不同城市的member——join——group存到不同的文件中
def saveCityMember():
    mem_grp_info=pd.read_csv(Const.MEMBER_PATH, encoding="iso-8859-1")[['member_id', 'city', 'group_id']]
    mem_grp_chicago=mem_grp_info.loc[mem_grp_info.iloc[:,1].str.contains(r'(.*)[C|c]hicago(.*)')]
    mem_grp_NY=mem_grp_info.loc[mem_grp_info.iloc[:,1].str.contains(r'(.*)[N|n]ew [Y|y]ork(.*)')]
    mem_grp_SF=mem_grp_info.loc[mem_grp_info.iloc[:,1].str.contains(r'(.*)[S|s]an [F|f]rancisco(.*)')]
    rd.to_csv_noindex(mem_grp_chicago,Const.MEM_GRP_CHI)
    rd.to_csv_noindex(mem_grp_NY,Const.MEM_GRP_NY)
    rd.to_csv_noindex(mem_grp_SF,Const.MEM_GRP_SF)

def dealCategoryShortname():
    cates=pd.read_csv(Const.GROUP_PATH)[['category_id','category.shortname']].drop_duplicates()
    cateSrc=pd.read_csv(Const.CTGY_PATH)
    cateSrc=pd.merge(cateSrc,cates)
    rd.to_csv_noindex(cateSrc,Const.CTGY_PATH)

# member类
class Member():
    def __init__(self, ID):
        self.id=ID
        self.vector=[]
    def toString(self):
        str='type: Member\n'
        str=str+'ID: %d\n' %(self.id)
        str=str+'vector: %s\n' %(self.vector)
        return str
# 计算会员之间的相似度
def rread_xlsx(PATH):
    df=pd.read_excel(PATH)
    df['member_id']=pd.Series(df['member_id'].fillna(method='ffill'))
    return df
def dealMemberSimilarity():
    chi_p='result/group_counts_percate_per_member_chicago.xlsx'
    sf_p='result/group_counts_percate_per_member_san_francisco.xlsx'
    ny_p='result/group_counts_percate_per_member_new_york.xlsx'
    mem_chi=rread_xlsx(chi_p)
    memgb=mem_chi.groupby('member_id')
    memgb=[memgb.get_group(x) for x in memgb.groups]
    members=[]
    for df in memgb:
        tempMem=Member(df['member_id'].values[0])
        tempMem.vector=df['counts'].values
        tempMem.city='Chicago Area'
        members.append(tempMem)
    print(members[0].toString())
# saveRealMembers()
# testMember()
# saveCityMember()
# selTop20()
# dealCategoryShortname()
# memberGroup()
dealMemberSimilarity()