import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *

city_path = 'data/cities.csv'
ctgy_path = 'data/categories.csv'
event_path = 'data/events.csv'
group_path = 'data/groups.csv'
topic_path = 'data/topics.csv'
grp_tpc_path = 'data/groups_topics.csv'
member_path = 'data/members.csv'
mmb_tpc_path = 'data/members_topics.csv'
venue_path = 'data/venues.csv'

def info_split(info, item):
    return info[item].value_counts()

city_info = pd.read_csv(city_path)
city_number = city_info.shape[0]
city_attributes = city_info.columns
city_attr_num = city_info.shape[1]
city_split = city_info['state'].value_counts()
# 每个州中城市的个数
# city_split.plot.bar()
#
# # 城市在坐标系中的位置
# x=city_info[city_attributes[4]]
# y=city_info[city_attributes[6]]
# fig=plt.figure()
# axes=fig.add_axes([0.1,0.1,0.8,0.8])
# axes.plot(x,y,'g+')
# axes.set_xlabel('x')
# axes.set_ylabel('y')
# axes.set_title('title')
# plt.show()

group_info = pd.read_csv(group_path)
group_num = group_info.shape[0]
group_attr_num = group_info.shape[1]
group_attrs = group_info.columns



# ranges = np.arange(0,5.5,0.5)
# group_rating=group_info['group_id'].groupby(pd.cut(group_info.rating, ranges)).count()
# group_rating.plot.bar()
# plt.show()
# groups per city
group_split_city = info_split(group_info,'city')
fig1 = plt.figure()
axes1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
axes1.bar(list(arange(len(group_split_city)) + 1), group_split_city)
axes1.xaxis.set_visible(False)
axes1.set_title('groups number per city')
# group_split_city.plot.bar()
for x, y, z in zip(np.arange(len(group_split_city)), group_split_city, group_split_city._index):
    plt.text(x + 1, y + 80, '%d' % y, ha='center', va='center')
    plt.text(x + 1, -400, z, ha='center', va='center', rotation=15)

# groups per category
group_split_category = info_split(group_info, 'category.shortname')
fig2 = plt.figure()
axes2 = fig2.add_axes(([0.1, 0.2, 0.8, 0.7]))
axes2.bar(arange(len(group_split_category)) + 1, group_split_category)
axes2.xaxis.set_visible(False)
axes2.set_title('groups number per category')
for x, y, z in zip(np.arange(len(group_split_category)), group_split_category, group_split_category._index):
    plt.text(x + 1, y + 80, '%d' % y, ha='center', va='center')
    plt.text(x + 1, -400, z, ha='center', va='center', rotation=60)

# groupby rating
ranges = np.arange(0,5.5,0.5)
group_rating=group_info['group_id'].groupby(pd.cut(group_info.rating, ranges)).count()
fig3=plt.figure()
axes3=fig3.add_axes([0.1,0.2,0.8,0.7])
axes3.set_title('groups number per rating')
for x,y in zip(np.arange(len(group_rating)), group_rating):
    plt.text(x, y+200, '%d' % y, ha='center', va='center')
# axes3.bar(group_rating._index,group_rating)
group_rating.plot.bar()
plt.show()
# group_split_category=group_info['category.shortname'].value_counts()
# print(group_split_category)
# group_split_category.plot.bar()
# for x,y in zip(np.arange(len(group_split_category)),group_split_category):
#     plt.text(x, y+10, '%.d' % y, ha='center', va='bottom')
# plt.show()


ctgy_info = pd.read_csv(ctgy_path)
category_num = ctgy_info.shape[0]
category_attr_num = ctgy_info.shape[1]
category_attrs = ctgy_info.columns
# print('category number: ', len(ctgy_info))

# event_info = pd.read_csv(event_path)
# print('event number: ', len(event_info))

# topic_info = pd.read_csv(topic_path, encoding = "iso-8859-1")
# print('topic number: ', len(topic_info))

# grp_tpc_info = pd.read_csv(grp_tpc_path, encoding = "iso-8859-1")
# print('group topic number: ', len(grp_tpc_info))

# member_info = pd.read_csv(member_path, encoding = "iso-8859-1")
# print('member number: ', len(member_info))

# mmb_tpc_info = pd.read_csv(mmb_tpc_path)
# print('member topic number: ', len(mmb_tpc_info))

# venue_info = pd.read_csv(venue_path)
# print('venue number: ', len(venue_info))
