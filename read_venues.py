import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

venues_info = pd.read_csv(Const.VENUE_PATH)
venue_at = rd.DataInfo(venues_info)
venue_at.to_excsv(Const.SIMPLE_PATH, item='venue')

rd.multiSplit(venues_info,['city'])

venue_city_Series = rd.info_split_merge(venues_info, 'city')
# venue_city_fig = rd.info_draw(venue_city_Series, 'venues number per city')
venue_state_Series = rd.info_split_merge(venues_info, 'state')
# venue_state_fig = rd.info_draw(venue_state_Series, 'venues number per state')
venue_rating_fig = rd.info_rating(venues_info)
venues_normalized_rating_fig = rd.info_rating(venues_info, groupedby='normalised_rating')
# venue_locations_fig = rd.info_locations(venues_info, 'lat', 'lon')
plt.show()
