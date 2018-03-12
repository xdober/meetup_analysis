import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

venues_info=pd.read_csv(Const.VENUE_PATH)
venue_at = rd.DataInfo(venues_info)
venue_at.to_excsv(Const.SIMPLE_PATH,item='venue')

venue_state_fig=rd.info_draw(venues_info,'state','venues number per state')
venue_city_fig=rd.info_draw(venues_info,'city','venues number per city')
venue_rating_fig=rd.info_rating(venues_info)
venues_normalized_rating_fig=rd.info_rating(venues_info,groupedby='normalised_rating')
venue_locations_fig=rd.info_locations(venues_info,'lat','lon')
plt.show()