import pandas as pd
import re
import matplotlib.pyplot as plt
from constant import Const
from pylab import *

# kw中如果order项值为index，则按照index排序，否则按value排序
def info_split(info, item, kw):
    if 'order' in kw:
        if kw['order'] == 'index':
            return info[item].value_counts().sort_index()
    return info[item].value_counts()


# 统计每个item取值的数量，并画出柱形图
# kw继续传递到info_splited中，决定排序的依据,notsave在此处决定是否把图形保存到文件
def info_draw(info, item, title=None, **kw):
    info_splited = info_split(info, item, kw)
    def findnames(name):
        names=[]
        for onename in info_splited.index:
            if re.search(name, onename,re.IGNORECASE):
                names.append(onename)
        return names
    list0=findnames('new york')
    print(list0)

    if 'merge' in kw:
        def merge_city():
            nonlocal info_splited
            info_splited['New York']+=info_splited['New York City']+info_splited['New York, NY']
            info_splited=info_splited.drop('New York City')

        switch_dict={
            'city': merge_city()
        }
        switch_dict.get(kw['merge'])

    fig_tmp = plt.figure()
    wid = len(info_splited) * 1.6
    left = 2.5 / wid
    fig_tmp.set_size_inches(wid, 10.5)
    axes_tmp = fig_tmp.add_axes([min(0.1, left), 0.1, 0.9 - min(0.1, left), 0.8])
    if not title:
        title = item
    axes_tmp.set_title(title)
    info_splited.plot.bar()
    plt.xticks(rotation='0')
    maxy = info_splited.max() / 50
    for x, y in zip(arange(len(info_splited)), info_splited):
        plt.text(x, y + maxy, '%d' % y, va='center', ha='center')
    if 'notsave' not in kw:
        plt.savefig('images/%s.pdf' % title, dpi=72, format='pdf')
    return fig_tmp


# 按照创建时间分组并画图
# kw中gap项决定分割的间隔，默认一年，若gap='month',则是一个月
# kw中created项决定使用哪一组数据，默认为'created'下标的一组
# kw中rotation项确定了横坐标系的文本旋转角度
def info_groupedby_created(gap, created, rotation, info, **kw):
    gapp = pd.to_datetime(info.created).dt.year
    if 'gap' in kw:
        if gap == 'month':
            gapp = [pd.to_datetime(info.created).dt.year, pd.to_datetime(info.created).dt.month]
    created = 'created'
    if 'created' in kw:
        created = created
    info_created = info[created].groupby(gapp).count()
    fig_tmp = plt.figure()
    wid = len(info_created) * 1.6
    heigh = info_created.max() / 80
    fig_tmp.set_size_inches(wid, 10.5)
    axes_tmp = fig_tmp.add_axes([0.1, 0.1, 0.8, 0.8])
    axes_tmp.set_title('%s number per year' % info.columns[0])
    info_created.plot.bar()
    if 'rotation' in kw:
        plt.xticks(rotation=rotation)
    for x, y in zip(np.arange(len(info_created)), info_created):
        plt.text(x, y + heigh, '%d' % y, ha='center', va='center')
    plt.savefig('images/%s number per year.pdf' % info.columns[0], dpi=72, format='pdf')
    return fig_tmp


# 画出评分的柱形图
# kw中by项确定了评分列
def info_rating(info, **kw):
    groupedby = 'rating'
    if 'by' in kw:
        groupedby = kw['by']
    ranges = np.arange(0, 5.5, 0.5)
    splited_rating = info[info.columns[0]].groupby(pd.cut(info[groupedby], ranges)).count()
    fig_tmp = plt.figure()
    wid3 = len(splited_rating) * 1.6
    height = splited_rating.max() / 80
    fig_tmp.set_size_inches(wid3, 10.5)
    axes3 = fig_tmp.add_axes([0.1, 0.2, 0.8, 0.8])
    axes3.set_title('groups number per rating')
    for x, y in zip(np.arange(len(splited_rating)), splited_rating):
        plt.text(x, y + height, '%d' % y, ha='center', va='center')
    splited_rating.plot.bar()
    plt.xticks(rotation='0')
    plt.savefig('images/%s number per %s.pdf' % (info.columns[0], groupedby), dpi=72, format='pdf')
    return fig_tmp


# 根据经纬度画散点图
def info_locations(info, lat, lon):
    lats = info[lat]
    lons = info[lon]
    fig_tmp = plt.figure()
    axes5 = fig_tmp.add_axes([0.1, 0.1, 0.8, 0.8])
    axes5.scatter(lats, lons, label='%s' % info.columns[0], s=4, alpha=0.02, linewidths=0)
    axes5.legend(loc='upper left')
    axes5.set_title('%s\'s location' % info.columns[0])
    axes5.set_xlabel('latitude')
    axes5.set_ylabel('longitude')
    plt.savefig('images/%s\'s location.pdf' % info.columns[0], dpi=72, format='pdf')
    return fig_tmp


class DataInfo(object):
    def __init__(self, info):
        self.length = len(info)
        self.attrs = list(info.columns.values)
        self.attrs_number = len(self.attrs)

    def to_excsv(self, PATH, **kw):
        item=self.attrs[0]
        if 'item' in kw:
            item=kw['item']
        simple=pd.read_csv(Const.SIMPLE_PATH)
        if not (item in simple['item'].values):
            df = pd.DataFrame(columns=['a', 'b', 'c', 'd'])
            df.loc[0] = {'a': item, 'b': self.length, 'c': self.attrs_number, 'd': self.attrs}
            with open(PATH, 'a') as f:
                df.to_csv(f, header=False, index=False)
                print('write 1 record!')