import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

group_topic_info = pd.read_csv(Const.GRP_TPC_PATH, encoding="iso-8859-1")
group = pd.read_csv(Const.GROUP_PATH)
topic = pd.read_csv(Const.TOPIC_PATH, encoding="iso-8859-1")
group_topic = pd.merge(group_topic_info[['topic_id', 'group_id']], group[['group_id','category_id','category.shortname']], on='group_id')
group_topic = pd.merge(group_topic,topic[['topic_id','main_topic_id','topic_name']],on='topic_id')
print(group_topic.head())
groupby_topic=group_topic.groupby(['main_topic_id   '])
print(groupby_topic.size())