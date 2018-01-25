import pandas as pd
import read_tools as rd
from constant import Const

topic_info=pd.read_csv(Const.TOPIC_PATH, encoding="iso-8859-1")
print(topic_info.shape)
topic_at=rd.DataInfo(topic_info)
topic_at.to_excsv(Const.SIMPLE_PATH,item='topic')