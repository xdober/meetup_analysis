import pandas as pd
import read_tools as rd
import numpy as np
from constant import Const
from pylab import *

# 把event信息按照group分组
def event_per_group(event_info):
    event_gb=event_info.groupby(['group_id'])
    events_per_group=[event_gb.get_group(x) for x in event_gb.groups]
    events_per_group.sort(key=len,reverse=True)
    print(events_per_group[30])
    return events_per_group
# 处理event信息
def dealEvents():
    event_info=pd.read_csv(Const.EVENT_PATH)
    events_per_group = event_per_group(event_info)
    event_created_fig = rd.info_groupedby_created(events_per_group[0], gap='month', notsave='yes', created='created')
    event_start_fig = rd.info_groupedby_created(events_per_group[0], gap='month', notsave='yes', created='event_time')
    plt.show()

# 简化event信息
def simplifyEvent():
    event_info=pd.read_csv(Const.EVENT_SIMP_PATH)[['event_id', 'created', 'duration', 'group_id', 'group.who', 'rsvp_limit', 'event_time', 'updated', 'utc_offset', 'venue.address_1', 'venue.city', 'venue_id', 'waitlist_count', 'yes_rsvp_count']]
    rd.to_csv_noindex(event_info,'data/event_simple.csv')

# simplifyEvent()
dealEvents()
