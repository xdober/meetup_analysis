import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

# 该模块尝试分析group的人数与event数量之间的关系
groups_info = pd.read_csv(Const.GROUP_PATH)
events_info = pd.read_csv(Const.EVENT_PATH)

grp_lite=groups_info[['group_id','category.shortname','city_id','members','group_name']]
evnt_lite=events_info[['event_id','group_id','venue_id']]
evnt_grp=pd.merge(evnt_lite,grp_lite,on='group_id',sort=False)
eg_ser=rd.info_split_merge(evnt_grp,'group_id')
eg_df=pd.DataFrame({'group_id':eg_ser.index, 'event_count':eg_ser.values})
eg_lite=pd.merge(eg_df,grp_lite,on='group_id')[['event_count', 'members','group_name']].set_index('group_name').head(20)
eg_lite_fig=rd.info_multi_draw(eg_lite,'event and member number per group',rotation=0)

# 每个类别的人数与event数量之间的对比
evnt_cate_ser=rd.info_split_merge(evnt_grp,'category.shortname')
evnt_cate_df=pd.DataFrame({'category':evnt_cate_ser.index, 'event_count':evnt_cate_ser.values})
member_cate_ser=grp_lite.groupby(by=['category.shortname'])['members'].sum()
member_cate_df=pd.DataFrame({'category':member_cate_ser.index, 'members':member_cate_ser.values})
evnt_member_df=pd.merge(evnt_cate_df,member_cate_df,on='category').set_index('category')
em_fig=rd.info_multi_draw(evnt_member_df,'event and member per category')
# eg_cate_fig=rd.info_draw(eg_cate_ser,'events number per group', notsave='yes')
plt.show()