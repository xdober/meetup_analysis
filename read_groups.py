import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

group_info = pd.read_csv(Const.GROUP_PATH)
group_at = rd.DataInfo(group_info)
group_at.to_excsv(Const.SIMPLE_PATH, item='group')
