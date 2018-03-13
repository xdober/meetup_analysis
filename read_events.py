import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

event_info = pd.read_csv(Const.EVENT_PATH)
event_at=rd.DataInfo(event_info)
event_at.to_excsv(Const.SIMPLE_PATH,item='event')

event_fee_series=rd.info_split_merge(event_info,'fee.required')
event_fee_fig = rd.info_draw(event_fee_series, 'event_fee_required')
event_state_series=rd.info_split_merge(event_info,'venue.state')
event_state_fig = rd.info_draw(event_state_series, 'event_venue_state')
event_city_series=rd.info_split_merge(event_info,'venue.city')
event_city_fig = rd.info_draw(event_city_series, 'event_venue_state')
event_info['duration']=event_info['duration']/3600
event_duration_series=rd.info_split_merge(event_info,'duration', order='index')
event_duration_fig = rd.info_draw(event_duration_series, 'event_duration')
event_pay_series=rd.info_split_merge(event_info,'fee.accepts')
event_pay_fig = rd.info_draw(event_pay_series, 'event fee accept')
event_visibility_series=rd.info_split_merge(event_info,'visibility')
event_visibility_fig = rd.info_draw(event_visibility_series, 'event visibility')
# event_state_fig = rd.info_draw(event_info, 'venue.state', 'event_venue_state')
# event_city_fig = rd.info_draw(event_info, 'venue.city', 'event_venue_city')
# event_info['duration']=event_info['duration']/3600
# event_duration_fig = rd.info_draw(event_info, 'duration', 'event_duration', order='index')
# event_pay_fig=rd.info_draw(event_info,'fee.accepts','event fee accept')
# event_group_fig=rd.info_draw(event_info,'group.name','event per group')
# event_groupwho_fig=rd.info_draw(event_info,'group.who','events number per who join')
event_created_fig=rd.info_groupedby_created(event_info,gap='month')
# event_visibility_fig = rd.info_draw(event_info, 'visibility', 'event_visibility')
plt.show()