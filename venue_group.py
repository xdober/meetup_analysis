import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

groups_info = pd.read_csv(Const.GROUP_PATH)
venues_info = pd.read_csv(Const.VENUE_PATH)

cities = ['west new york', 'New York', 'Chicago Ridge', 'Chicago Heights', 'ChicagoTinley Park', 'Chicagoland',
          'east chicago', 'Rolling MeadowsChicago', 'ChicagoWoodstock', 'Northlake', 'North Chicago', 'Chicago',
          'S San Francisco', 'South San Francisco', 'San Francisco']
# venue_city_fig=rd.info_draw(venues_info,'city','venues number per city', cities,notsave='yes', merge='city', rotation=20)
# group_city_fig=rd.info_draw(groups_info,'city','groups number per city',notsave='yes')
venue_city_series = rd.info_split_merge(venues_info, 'city', cities, merge='city')
venue_city_series.name = 'venue'
# venue_city_fig=rd.info_draw(venue_city_series,'venues number per city',notsave='yes', rotation=20)
group_city_series = rd.info_split_merge(groups_info, 'city', cities, merge='city')
group_city_series.name = 'group'
# group_city_fig=rd.info_draw(group_city_series,'group number per city',notsave='yes', rotation=20)

venue_group_info = pd.concat([venue_city_series, group_city_series], axis=1, names=['venue', 'group']).sort_values(
    by='venue', ascending=False)
venue_group_fig = rd.info_multi_draw(venue_group_info, 'venue group per city', rotation=25)
print(venue_group_info)

plt.show()
