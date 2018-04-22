import pandas as pd
import read_tools as rd
import numpy as np
from constant import Const

# 把event信息按照group分组
def event_per_group():
    event_info=pd.read_csv(Const.EVENT_PATH)
    event_gb=event_info.groupby(['group_id'])
    events_per_group=[event_gb.get_group(x) for x in event_gb.groups]


