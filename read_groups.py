import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

group_info = pd.read_csv(Const.GROUP_PATH)
group_at = rd.DataInfo(group_info)
group_at.to_excsv(Const.SIMPLE_PATH, item='group')

# city_sl=rd.info_split_merge(group_info,'city')
# rd.to_csv_index(city_sl,'result/groups_per_city.csv')
sers=rd.multiSplit(group_info,['city','category.shortname'])
print(sers)