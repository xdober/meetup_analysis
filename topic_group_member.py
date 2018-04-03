import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

group_topic_info = pd.read_csv(Const.GRP_TPC_PATH, encoding="iso-8859-1")
group = pd.read_csv(Const.GROUP_PATH)
topic = pd.read_csv(Const.TOPIC_PATH, encoding="iso-8859-1")
group_topic = pd.merge(group_topic_info, group, on='group_id')[['topic_id', 'topic_key', 'topic_name', 'group_id', 'category_id', 'category.shortname']]
# grouped_topic_group = group_topic.groupby(['topic_id', 'topic_name', 'category.shortname']).size().reset_index(name='group_counts').sort_values('group_counts', ascending=False)
grouped_topic = group_topic.groupby(['topic_id', 'topic_name']).size().reset_index(name='group_counts').sort_values('group_counts', ascending=False)

grouped_topic = pd.merge(grouped_topic, topic, on=['topic_id', 'topic_name'])[['topic_id', 'topic_name', 'group_counts', 'members', 'main_topic_id']]
grouped_topic = pd.merge(grouped_topic, topic[['topic_id', 'topic_name', 'urlkey']], left_on='main_topic_id',right_on='topic_id')
# grouped_topic.to_csv(Const.TPC_GRPBY_PATH, sep=',', index=False)
# rd.to_csv_noindex(grouped_topic_group, Const.TPC_GRP_GRPBY_PATH)
ngroupby = grouped_topic.groupby(['main_topic_id','topic_name_y']).sum().reset_index().sort_values('group_counts',ascending=False)
ngroupby=ngroupby[['main_topic_id','topic_name_y','group_counts','members']]
ngroupby=ngroupby.rename(index=str,columns={'topic_name_y':'topic_name'})
rd.to_csv_noindex(ngroupby,Const.TPC_GRP_TPC_PATH)
print(ngroupby)
