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


# 按照item将info分类计数，如果merges不为[]则需要合并含有相同关键词的项
# return 类型为Series[name, count]
def info_split_merge(info, item, merges=[], **kw):
    info_splited = info_split(info, item, kw)
    ninfo_splited = info_splited

    def findnames(name):
        names = []
        for onename in info_splited.index:
            if re.search(name, onename, re.IGNORECASE):
                names.append(onename)
        return names

    if 'merge' in kw:
        ninfo_splited = pd.Series([], [])

        def merge_cities(cities):
            nonlocal ninfo_splited
            # print(cities)
            for one_city in cities:
                merge_one_city(one_city)
            ninfo_splited = ninfo_splited.sort_values(ascending=False)

        def merge_one_city(city_name):
            nonlocal info_splited, ninfo_splited
            lists = findnames(city_name)
            num = 0
            for item in lists:
                num += info_splited[item]
                info_splited = info_splited.drop(item)
            ninfo_splited = ninfo_splited.append(pd.Series([num], index=[city_name]))
            # print('merged %s: %d' % (city_name ,num))

        switch_dict = {
            'city': merge_cities,
            'who': merge_cities
        }

        switch_dict.get(kw['merge'])(merges)
    return ninfo_splited


# 根据给定的Series画出柱形图
# ninfo_splited为Series对象，其index为name, value为int; title为标题/文件名
# **kw中notsave在此处决定是否把图形保存到文件，rotation决定x轴坐标文字的旋转角度（逆时针）
def info_draw(ninfo_splited, title, **kw):
    fig_tmp = plt.figure()
    wid = len(ninfo_splited) * 1.6
    left = 2.5 / wid
    fig_tmp.set_size_inches(wid, 10.5)
    axes_tmp = fig_tmp.add_axes([min(0.1, left), 0.1, 0.9 - min(0.1, left), 0.8])
    axes_tmp.set_title(title)
    ninfo_splited.plot.bar()
    plt.xticks(rotation='0')
    maxy = ninfo_splited.max() / 50
    if 'rotation' in kw:
        plt.xticks(rotation=kw['rotation'])
    for x, y in zip(arange(len(ninfo_splited)), ninfo_splited):
        plt.text(x, y + maxy, '%d' % y, va='center', ha='center')
    if 'notsave' not in kw:
        plt.savefig('images/%s.pdf' % title, dpi=72, format='pdf')
    return fig_tmp


# 画多个柱
def info_multi_draw(info, title, **kw):
    fig_tmp = plt.figure()
    wid = len(info) * 1.6
    left = 2.5 / wid
    fig_tmp.set_size_inches(wid, 10.5)
    axes_tmp = fig_tmp.add_axes([min(0.1, left), 0.1, 0.9 - min(0.1, left), 0.8])
    width = 0.35
    axes_tmp.set_title(title)
    x = np.arange(len(info))
    yn = len(info.columns)
    ys = []
    for i in range(0, yn):
        ys.append(info.ix[:, i])
        axes_tmp.bar(x + width * i, ys[i], width)
        maxy = ys[i].max() / 50
        for xx, y in zip(arange(len(info)), ys[i].values):
            plt.text(xx + width * i, y + maxy, '%d' % y, va='center', ha='center')
    axes_tmp.set_xticks(x + width * (yn - 1) / 2)
    axes_tmp.set_xticklabels(info.index)
    if 'rotation' in kw:
        plt.xticks(rotation=kw['rotation'])
    if 'notsave' not in kw:
        plt.savefig('images/%s.pdf' % title, dpi=72, format='pdf')
    return fig_tmp


# 按照创建时间分组并画图
# kw中gap项决定分割的间隔，默认一年，若gap='month',则是一个月
# kw中created项决定使用哪一组数据，默认为'created'下标的一组
# kw中rotation项确定了横坐标系的文本旋转角度
# def info_groupedby_created(gap, created, rotation, info, **kw):
def info_groupedby_created(info, **kw):
    gapp = pd.to_datetime(info.created).dt.year
    if 'gap' in kw:
        if kw['gap'] == 'month':
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
        plt.xticks(rotation=kw['rotation'])
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

# 画饼图
def info_pie(df, ranges, labels, title, **kw):
    df=pd.DataFrame({'INDEX':df.index,'COUNT':df.values})
    fig_tmp = plt.figure()
    axes0 = fig_tmp.add_axes([0.1, 0.1, 0.8, 0.8])
    dfed = df.groupby(pd.cut(df['INDEX'], ranges)).sum()
    dfed=dfed.replace(NaN,0)
    print(dfed)
    axes0.pie(dfed['COUNT'].values, labels=labels, autopct='%1.1f%%')
    axes0.set_title(title)
    if 'notsave' not in kw:
        plt.savefig('images/%s.pdf' % title, dpi=72, format='pdf')
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
        item = self.attrs[0]
        if 'item' in kw:
            item = kw['item']
        simple = pd.read_csv(Const.SIMPLE_PATH)
        if not (item in simple['item'].values):
            df = pd.DataFrame(columns=['a', 'b', 'c', 'd'])
            df.loc[0] = {'a': item, 'b': self.length, 'c': self.attrs_number, 'd': self.attrs}
            with open(PATH, 'a') as f:
                df.to_csv(f, header=False, index=False)
                print('write 1 record!')
