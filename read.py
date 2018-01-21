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


# 统计每个item取值的数量，并画出柱形图
def info_draw(info, item, title=None):
    info_splited = info_split(info, item)
    fig_tmp = plt.figure()
    axes_tmp = fig_tmp.add_axes([0.1, 0.1, 0.8, 0.8])
    if not title :
        title=item
    axes_tmp.set_title(title)
    info_splited.plot.bar()
    plt.xticks(rotation='0')
    maxy = info_splited.max() / 50
    for x, y in zip(arange(len(info_splited)), info_splited):
        plt.text(x, y + maxy, '%d' % y, va='center', ha='center')
    plt.savefig('images/'+title+'.png')
    return fig_tmp


city_info = pd.read_csv(city_path)
city_number = city_info.shape[0]
city_attributes = city_info.columns
city_attr_num = city_info.shape[1]
city_split = city_info['state'].value_counts()
# 每个州中城市的个数
# city_split.plot.bar()
#
# # # 城市在坐标系中的位置
# x = city_info[city_attributes[4]]
# y = city_info[city_attributes[6]]
# fig0 = plt.figure()
# axes0 = fig0.add_axes([0.1, 0.1, 0.8, 0.8])
# axes0.scatter(x, y, s=35,marker='*',linewidths=2,label='cities')
# axes0.legend(loc='upper left')
# axes0.set_xlabel('latitude')
# axes0.set_ylabel('longitude')
# axes0.set_title('cities\' location')

group_info = pd.read_csv(group_path)
group_num = group_info.shape[0]
group_attr_num = group_info.shape[1]
group_attrs = group_info.columns

# ranges = np.arange(0,5.5,0.5)
# group_rating=group_info['group_id'].groupby(pd.cut(group_info.rating, ranges)).count()
# group_rating.plot.bar()
# plt.show()
# # groups per city
# group_split_city = info_split(group_info,'city')
# fig1 = plt.figure()
# axes1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
# axes1.bar(list(arange(len(group_split_city)) + 1), group_split_city)
# axes1.xaxis.set_visible(False)
# axes1.set_title('groups number per city')
# for x, y, z in zip(np.arange(len(group_split_city)), group_split_city, group_split_city._index):
#     plt.text(x + 1, y + 80, '%d' % y, ha='center', va='center')
#     plt.text(x + 1, -400, z, ha='center', va='center', rotation=15)
#
# # groups per category
# group_split_category = info_split(group_info, 'category.shortname')
# fig2 = plt.figure()
# axes2 = fig2.add_axes(([0.1, 0.2, 0.8, 0.7]))
# axes2.bar(arange(len(group_split_category)) + 1, group_split_category)
# axes2.xaxis.set_visible(False)
# axes2.set_title('groups number per category')
# for x, y, z in zip(np.arange(len(group_split_category)), group_split_category, group_split_category._index):
#     plt.text(x + 1, y + 80, '%d' % y, ha='center', va='center')
#     plt.text(x + 1, -400, z, ha='center', va='center', rotation=60)
#
# # groupby rating
# ranges = np.arange(0,5.5,0.5)
# group_rating=group_info['group_id'].groupby(pd.cut(group_info.rating, ranges)).count()
# fig3=plt.figure()
# axes3=fig3.add_axes([0.1,0.2,0.8,0.7])
# axes3.set_title('groups number per rating')
# for x,y in zip(np.arange(len(group_rating)), group_rating):
#     plt.text(x, y+200, '%d' % y, ha='center', va='center')
# group_rating.plot.bar()

# # groupby created date
# group_created = group_info['group_id'].groupby(pd.to_datetime(group_info.created).dt.year).count()
# fig4 = plt.figure()
# axes4 = fig4.add_axes([0.1, 0.1, 0.8, 0.8])
# axes4.set_title('groups number per year')
# group_created.plot.bar()
# for x, y in zip(np.arange(len(group_created)), group_created):
#     plt.text(x, y + 100, '%d' % y, ha='center', va='center')
#
# # groups number per state
# group_state_fig = info_draw(group_info, 'state', 'groups number per state')

# # groups' location
# lats=group_info['lat']
# lons=group_info['lon']
# fig5=plt.figure()
# axes5=fig5.add_axes([0.1,0.1,0.8,0.8])
# axes5.scatter(lats,lons,label='groups', s=10)
# axes5.legend(loc='upper left')
# axes5.set_title('groups\' location' )
# axes5.set_xlabel('latitude')
# axes5.set_ylabel('longitude')

# organizer
group_org=info_split(group_info,'organizer.member_id')
print(group_org.head())

# who
group_who=info_split(group_info,'who')
print(group_who.head())

# join_mode
group_join_mode=info_split(group_info,'join_mode')
group_join_mode_fig=info_draw(group_info,'join_mode')

# visibility
group_visiblity_fig=info_draw(group_info,'visibility')

# state
group_state_fig=info_draw(group_info,'state')

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
