import pandas as pd
import matplotlib.pyplot as plt
from pylab import *


def info_split(info, item):
    return info[item].value_counts()


# 统计每个item取值的数量，并画出柱形图
def info_draw(info, item, title=None):
    info_splited = info_split(info, item)
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

def info_groupedby_created(info,created='created', gap='year'):
    info_created = info[created].groupby(pd.to_datetime(info.created).dt.year).count()
    fig_tmp = plt.figure()
    wid = len(info_created) * 1.6
    fig_tmp.set_size_inches(wid, 10.5)
    axes4 = fig_tmp.add_axes([0.1, 0.1, 0.8, 0.8])
    axes4.set_title('%s number per year'  % info.columns[0])
    info_created.plot.bar()
    plt.xticks(rotation='0')
    for x, y in zip(np.arange(len(info_created)), info_created):
        plt.text(x, y + 100, '%d' % y, ha='center', va='center')
    plt.savefig('images/%s number per year.pdf' % info.columns[0], dpi=72, format='pdf')
    return fig_tmp