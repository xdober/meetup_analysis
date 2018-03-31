import pandas as pd
import read_tools as rd
from constant import Const
from pylab import *

Arts_event = pd.read_csv(Const.ART_EVENT_DATA_PATH)
Career_event = pd.read_csv(Const.CAREER_EVENT_DATA_PATH)
Book_event = pd.read_csv(Const.BOOK_EVENT_DATA_PATH)

class du_fig():
    def __init__(self,Bar,Pie):
        self.Bar=Bar
        self.Pie=Pie

def df_to_ser(df,title):
    df['duration'] = df['duration'] / 3600
    duration_ser = rd.info_split_merge(df, 'duration', order='index')
    duration_bar=rd.info_draw(duration_ser,title+' event duration')
    duration_pie=rd.info_pie(duration_ser,[0,1.5,2.5,3.5,inf],['0~1.5','1.5~2.5','2.5~3.5','3.5~inf'],title+' duration pie')
    duration_fig=du_fig(duration_bar,duration_pie)
    return duration_fig

def nlen(strr):
    return len(str(strr))

# average duration per description range
def average_duration(df,column,ranges):
    ave=df.groupby(pd.cut(df[column],ranges)).mean()
    ave=ave.replace(NaN,0)
    ave=ave.loc[ave['des_len']!=0]
    ave['duration']=ave['duration'].map(lambda x:x/3600)
    return ave
# Art_fig=df_to_ser(Arts_event,'Art')
# Career_fig=df_to_ser(Career_event,'Career')
# Book_fig=df_to_ser(Book_event,'Book')

# Book_event['des_len']=Book_event['description'].map(nlen)
# Book_ave=average_duration(Book_event[['des_len','duration']],'des_len',np.arange(0,5600,100))
# bfig=rd.info_multi_draw(Book_ave,'duration per des',notsave='yes')

Career_event['des_len']=Career_event['description'].map(nlen)
Career_ave=average_duration(Career_event[['des_len','duration']],'des_len',np.arange(0,9000,100))
cfig=rd.info_multi_draw(Career_ave,'duration per des',notsave='yes')

print(Career_ave)

plt.show()