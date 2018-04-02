import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

topic_info=pd.read_csv(Const.TOPIC_PATH, encoding="iso-8859-1")
topic_group_info=pd.read_csv(Const.GRP_TPC_PATH, encoding="iso-8859-1")
# print(topic_info.shape)
# topic_at=rd.DataInfo(topic_info)
# topic_at.to_excsv(Const.SIMPLE_PATH,item='topic')
tpc_grp_ser=rd.info_split_merge(topic_group_info,'topic_id')
tpc_grp_df=pd.DataFrame({'parent_topic_id':tpc_grp_ser.index,'groups':tpc_grp_ser.values})
topic_main_ser=rd.info_split_merge(topic_info,'main_topic_id')
topic_main_df=pd.DataFrame({'parent_topic_id':topic_main_ser.index,'sub_topics':topic_main_ser.values})
topic_main_df=pd.merge(topic_main_df,tpc_grp_df,on='parent_topic_id',sort=False)
topic_main_df=pd.merge(topic_main_df,topic_info,left_on='parent_topic_id',right_on='topic_id').sort_values('groups',ascending=False)
topic_main_df=topic_main_df[['parent_topic_id','topic_name','members','groups','sub_topics','description','link','urlkey']]
# topic_main_df.to_csv(Const.TOPIC_SUBTOPIC_PATH,sep=',',index=False)
topic_main_df=topic_main_df[['topic_name','members','groups','sub_topics']].set_index('topic_name')
topic_main_df['members']=topic_main_df['members']/15000.0
topic_main_fig=rd.info_multi_draw(topic_main_df,'members and subtopics per topic',notsave='yes')


plt.show()