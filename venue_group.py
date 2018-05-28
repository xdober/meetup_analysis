import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

groups_info = pd.read_csv(Const.GROUP_PATH)
venues_info = pd.read_csv(Const.VENUE_PATH)

cities = ['New York', 'Chicago', 'San Francisco']
venue_city_series = rd.info_split_merge(venues_info, 'city', cities, merge='city')
venue_city_series.name = 'venue'
venue_city_series = venue_city_series.rename(lambda x: x + ' Area')
# print(venue_city_series)
venue_city_fig = rd.info_draw(venue_city_series, 'venues number per city', notsave='yes')
group_city_series = rd.info_split_merge(groups_info, 'city', cities, merge='city')
group_city_series.name = 'group'
group_city_series = group_city_series.rename(lambda x: x + ' Area')
# print(group_city_series)
group_city_fig = rd.info_draw(group_city_series, 'group number per city', notsave='yes')

venue_group_info = pd.concat([venue_city_series, group_city_series], axis=1, names=['venue', 'group']).sort_values(
    by='venue', ascending=False)
venue_group_fig = rd.info_multi_draw(venue_group_info, 'venue group per city')
rd.to_csv_index(venue_group_info,'result/venue_and_group_per_area.csv')
# print(venue_group_info)

plt.show()
