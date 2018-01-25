import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

category_info=pd.read_csv(Const.CTGY_PATH)
category_at=rd.DataInfo(category_info)
category_at.to_excsv(Const.SIMPLE_PATH,item='category')