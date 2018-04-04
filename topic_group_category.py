import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

group_topic_info = pd.read_csv(Const.GRP_TPC_PATH, encoding="iso-8859-1")
group = pd.read_csv(Const.GROUP_PATH)
topic = pd.read_csv(Const.TOPIC_PATH, encoding="iso-8859-1")

# 把一个maintopic下的群组按照category分类，并返回序列
def gbgbcate(df):
    nGB=rd.info_split_merge(df,'category.shortname')
    nGB.name=df['topic_name'].values[0]
    return nGB
# 试图分析每一个main_topic的关联群组中category的关系
group_topic = pd.merge(group_topic_info[['topic_id', 'group_id']], group[['group_id','category_id','category.shortname']], on='group_id')
group_topic = pd.merge(group_topic,topic[['topic_id','main_topic_id','topic_name']],on='topic_id')
group_topic=pd.merge(group_topic[['main_topic_id','group_id','category_id','category.shortname']],topic[['topic_id','topic_name']],left_on='main_topic_id',right_on='topic_id')[['main_topic_id','topic_name','group_id','category_id','category.shortname']]
print(group_topic.head())
groupby_topic=group_topic.groupby(['main_topic_id'])
# 把groupby对象转为df组成的list
gb=[groupby_topic.get_group(x) for x in groupby_topic.groups]
for x in range(0,len(gb)):
    print(gbgbcate(gb[x]).head())
