import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

member_info = pd.read_csv(Const.MEMBER_PATH, encoding="iso-8859-1")
member_at = rd.DataInfo(member_info)
# item=['member']
# records_number=[member_at.length]
# attrs_number_per_record=[member_at.attrs_number]
# attrs=[member_at.attrs]
df = pd.DataFrame(columns=['item', 'records_number', 'attrs_number_per_record', 'attrs'])
df.loc[len(df)] = {'item': 'member', 'records_number': member_at.length,
                   'attrs_number_per_record': member_at.attrs_number, 'attrs': member_at.attrs}
print(member_at.attrs)
df.to_csv('result/simple.csv', sep=',', index=False)

# 该份数据中有多少个成员，每个成员加入了几个组
# groups_per_member = rd.info_split(member_info, 'member_id', {})
df1 = pd.DataFrame({"count":member_info.groupby([member_info['member_id'],member_info['city']]).size()})
df1.to_csv(Const.GROUP_PER_MEMBER)

# 有多少个组，每个组有多少成员
# members_per_group = rd.info_split(member_info, 'group_id', {})
df2 = pd.DataFrame({"count":member_info.groupby(member_info['group_id']).size()})
df2.to_csv(Const.MEMBER_PER_GROUP)
