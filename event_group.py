import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

# 该模块尝试分析group的人数与event数量之间的关系
groups_info = pd.read_csv(Const.GROUP_PATH)
events_info = pd.read_csv(Const.EVENT_PATH)

# 画每个组的活动数与人数的柱形图，并返回结果
# 输入：活动信息，群组信息，范围（给活动数按一定范围分组）
# 返回：[柱形图fig,按ranges分好组的每个范围内的平均活动数和人数 , DataFrame（组名，活动数，人数）]
def event_per_group(event_info, group_info,ranges,title):
    event_lite=event_info[['event_id','group_id']]
    group_lite=group_info[['group_id','group_name','members']]
    event_group=pd.merge(event_lite,group_lite,on='group_id',sort=False)
    eg_ser=rd.info_split_merge(event_group,'group_id')
    eg_df=pd.DataFrame({'group_id':eg_ser.index,'event':eg_ser.values})
    eg_lite=pd.merge(eg_df,group_lite,on='group_id')[['event', 'members','group_name']].set_index('group_name')
    eg_lite_fig=rd.info_multi_draw(eg_lite.head(20),title,notsave='yes')

    eg_range=eg_lite.groupby(pd.cut(eg_lite['event'],ranges)).mean()
    return [eg_lite_fig,eg_range,eg_lite]

def event_menber_pie(df,midtop,title,**kw):
    fig_tmp=plt.figure()
    axes0=fig_tmp.add_axes([0.05, 0.1, 0.45, 0.8])
    axes1=fig_tmp.add_axes([0.5, 0.1, 0.45, 0.8])
    dfed=df.groupby(pd.cut(df['event'],[0,midtop,inf])).sum()
    labels=['less event','more event']
    axes0.pie(dfed['event'].values,labels=labels,autopct='%1.1f%%')
    axes0.set_title('event percentage')
    axes1.pie(dfed['members'].values,labels=labels,autopct='%1.1f%%')
    axes1.set_title('member percentage')
    if 'notsave' not in kw:
        plt.savefig('images/%s.pdf' % title, dpi=72, format='pdf')
    return fig_tmp
# # 每个群组event和member的对比
# grp_lite=groups_info[['group_id','category.shortname','city_id','members','group_name']]
# evnt_lite=events_info[['event_id','group_id','venue_id']]
# evnt_grp=pd.merge(evnt_lite,grp_lite,on='group_id',sort=False)
# eg_ser=rd.info_split_merge(evnt_grp,'group_id')
# eg_df=pd.DataFrame({'group_id':eg_ser.index, 'event_count':eg_ser.values})
# eg_lite=pd.merge(eg_df,grp_lite,on='group_id')[['event_count', 'members','group_name']].set_index('group_name')
# eg_lite_fig=rd.info_multi_draw(eg_lite.head(20),'event and member number per group',rotation=0)
# eg_lite.to_csv(Const.E_M_GROUP_PATH,sep=',')

# # 每个类别的人数与event数量之间的对比
# evnt_cate_ser=rd.info_split_merge(evnt_grp,'category.shortname')
# evnt_cate_df=pd.DataFrame({'category':evnt_cate_ser.index, 'event_count':evnt_cate_ser.values})
# member_cate_ser=grp_lite.groupby(by=['category.shortname'])['members'].sum()
# member_cate_df=pd.DataFrame({'category':member_cate_ser.index, 'members':member_cate_ser.values})
# evnt_member_df=pd.merge(evnt_cate_df,member_cate_df,on='category').set_index('category')
# em_fig=rd.info_multi_draw(evnt_member_df,'event and member per category')
# evnt_member_df.to_csv(Const.E_M_CATE_PATH,sep=',')

# # event per city
# cities=['New York','San Francisco','Chicago']
# event_city_ser=rd.info_split_merge(events_info,'venue.city',cities,merge='cities')
# event_city_fig=rd.info_draw(event_city_ser,'event per city')

# # who join the most events
# whos=['Artist', 'Toastmaster', 'Reader','women','school']
# event_who_series=rd.info_split_merge(events_info,'group.who',whos,merge='who')
# event_who_fig = rd.info_draw(event_who_series, 'events number per who join', notsave='yes')

# 同一类别中event数量与group人数的关系
Arts_group=groups_info.loc[groups_info['category_id']==1]
Arts_event=events_info.loc[events_info['group_id'].isin(Arts_group['group_id'].values)]
Art_arange = [0, 50, 150, 300]
[Arts_fig,Arts_ranges,Arts_eg]=event_per_group(Arts_event,Arts_group,Art_arange,'event per group (Arts category)')
Career_group=groups_info.loc[groups_info['category_id']==2]
Career_event=events_info.loc[events_info['group_id'].isin(Career_group['group_id'].values)]
Career_arange=[0,50,100,inf]
[Career_fig,Career_ranges,Career_eg]=event_per_group(Career_event,Career_group,Career_arange,'event per group (Career category)')
Book_group=groups_info.loc[groups_info['category_id']==18]
Book_event=events_info.loc[events_info['group_id'].isin(Book_group['group_id'].values)]
Book_arange=[0,10,100]
[Book_fig,Book_ranges,Book_eg]=event_per_group(Book_event,Book_group,Book_arange,'event per group (Book category)')
Arts_eg_pie=event_menber_pie(Arts_eg,50,'event and member percentage (Arts category)')
# Career_eg_pie=event_menber_pie(Book_eg,13)
Book_eg_pie=event_menber_pie(Book_eg,13,'event and member percentage (Book category)')
# print(Arts_ranges)
# print(Career_ranges)
# print(Book_ranges)

plt.show()