import pandas as pd
import matplotlib.pyplot as plt
from pylab import *


def info_split(info, item, kw):
    if 'order' in kw:
        if kw['order'] == 'index':
            return info[item].value_counts().sort_index()
    return info[item].value_counts()


# 统计每个item取值的数量，并画出柱形图
def info_draw(info, item, title=None, **kw):
    info_splited = info_split(info, item, kw)
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
    plt.savefig('images/%s.pdf' % title, dpi=72, format='pdf')
    return fig_tmp


# 按照创建时间分组并画图
def info_groupedby_created(info, **kw):
    gapp = pd.to_datetime(info.created).dt.year
    if 'gap' in kw:
        if kw['gap'] == 'month':
            gapp = [pd.to_datetime(info.created).dt.year, pd.to_datetime(info.created).dt.month]
    created = 'created'
    if 'created' in kw:
        created = kw['created']
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
