import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

event_info = pd.read_csv(Const.EVENT_PATH)
event_number = event_info.shape[0]
event_attrs = event_info.columns
event_attr_num = event_info.shape[1]

event_fee_fig = rd.info_draw(event_info, 'fee.required', 'event_fee_required')
event_state_fig = rd.info_draw(event_info, 'venue.state', 'event_venue_state')
event_info['duration']=event_info['duration']/3600
event_duration_fig = rd.info_draw(event_info, 'duration', 'event_duration')
event_created_fig=rd.info_groupedby_created(event_info)
plt.show()