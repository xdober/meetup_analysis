import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
# from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import read_tools as rd

def acfAndPacf(ser):
    print(ser)
    decomposition = seasonal_decompose(ser, model="additive")

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    log_nums=np.log(ser)
    plt.plot(trend)
    plt.plot(seasonal)
    plt.plot(residual,'r--')
    # plt.plot(log_nums)
    diff=ser.diff()
    diff2=diff.diff()
    # plot_acf(ser)
    plt.plot(ser)
    plt.plot(seasonal+trend,'c--')
    # plt.plot(diff)
    # plt.plot(diff2)
    plt.show()

df_weekly=pd.read_csv('data/NewAndTotalGroupCountsTrends_PerWeek.csv')
df=pd.read_csv('data/NewAndTotalGroupCountsTrends.csv')
df['simple_date']=pd.to_datetime(df['simple_date'])
df_weekly['simple_date']=pd.to_datetime(df['simple_date'])
df.set_index('simple_date',inplace=True)
df_weekly.set_index('simple_date',inplace=True)
print(df)
new_data=df['new']
new_weekly=df_weekly['new']
total_data=df['total']
total_weekly=df_weekly['total']
print(new_data)
for ser in [new_data]:
    acfAndPacf(ser)

plt.show()