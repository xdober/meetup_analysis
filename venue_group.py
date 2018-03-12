import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

# groups_info=pd.read_csv(Const.GROUP_PATH)
venues_info=pd.read_csv(Const.VENUE_PATH)

venue_city_fig=rd.info_draw(venues_info,'city','venues number per city',notsave='yes', merge='city')
plt.show()