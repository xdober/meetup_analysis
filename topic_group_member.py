import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

group_topic_info=pd.read_csv(Const.GRP_TPC_PATH, encoding="iso-8859-1")
group=pd.read_csv(Const.GROUP_PATH)
group_topic=pd.merge(group_topic_info,group,on='group_id')[['topic_id','topic_key','topic_name','group_id','category_id','category.shortname']]
grouped_topic_group=group_topic.groupby(['topic_name','category.shortname'])
grouped_topic=group_topic.groupby('topic_name')
# print(grouped_topic_group.size())
print(grouped_topic.count()\
      .reset_index()
      .sort_values('group_id',ascending=False))
