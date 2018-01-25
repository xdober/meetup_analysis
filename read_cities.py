import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

city_info=pd.read_csv(Const.CITY_PATH)
city_at=rd.DataInfo(city_info)
city_at.to_excsv(Const.SIMPLE_PATH,item='city')