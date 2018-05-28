import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
import read_tools as rd

# 平稳性检测
def test_stationarity(timeseries):
    dftest = adfuller(timeseries, autolag='AIC')
    return dftest[1]

def get_columns(df):
    columns=df.columns.values[1:]
    return  columns
# 使用多项式回归模型
def train_and_predict_one_column(aryset,pre=False):
    y=aryset.values
    x=range(0,len(y))
    # 读取完数据后，将它们转化为 Numpy 数组以方便进一步的处理
    x, y = np.array(x), np.array(y)
    x=x.reshape(-1,1)
    y=y.reshape(-1,1)
    # 随机分割训练集和测试集
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.25)
    # 将原始数据以散点图的形式画出
    # plt.figure()
    plt.scatter(xtrain, ytrain, c="g", s=5)
    plt.scatter(xtest, ytest, c="r", s=5)

    pol = PolynomialFeatures(degree=5)
    # 对训练集进行拟合标准化处理
    if True==pre:
        xtrain,ytrain=x,y
        xtest=np.arange(len(xtrain),len(xtrain)+30)
        xtest=xtest.reshape(-1,1)

    xtrain_pol = pol.fit_transform(xtrain)
    # 模型初始化
    lr_pol = LinearRegression()
    # 拟合
    lr_pol.fit(xtrain_pol, ytrain)
    if lr_pol.coef_[0][-1]<0:
        pol = PolynomialFeatures(degree=4)
        xtrain_pol = pol.fit_transform(xtrain)
    lr_pol.fit(xtrain_pol, ytrain)
    if True==pre:
        ytest=lr_pol.predict(pol.transform(xtest))
        x=np.concatenate((xtrain,xtest),axis=0)
        y=np.concatenate((lr_pol.predict(pol.transform(xtrain)),ytest),axis=0)
    r_score_pol = lr_pol.score(pol.transform(xtrain), ytrain)
    plt.plot(x, y, 'r-')
    return [lr_pol.coef_,r_score_pol,ytest]
# 使用逻辑回归模型
def logisticPredict(aryset):
    y = aryset.values
    x = range(0, len(y))
    # 读取完数据后，将它们转化为 Numpy 数组以方便进一步的处理
    x, y = np.array(x), np.array(y)
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    # 随机分割训练集和测试集
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.25)
    # 将原始数据以散点图的形式画出
    plt.figure()
    plt.scatter(xtrain, ytrain, c="g", s=5)
    plt.scatter(xtest, ytest, c="r", s=5)
    logi_model=LogisticRegression()
    logi_model.fit(xtrain,ytrain)
    y_pre=logi_model.predict_proba(x)
    plt.plot(x,y_pre,'r-')
# 使用岭回归模型
def RidgePredict(aryset):
    y = aryset.values
    x = range(0, len(y))
    # 读取完数据后，将它们转化为 Numpy 数组以方便进一步的处理
    x, y = np.array(x), np.array(y)
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    # 随机分割训练集和测试集
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.25)
    # 将原始数据以散点图的形式画出
    # plt.figure()
    plt.scatter(xtrain, ytrain, c="g", s=5)
    plt.scatter(xtest, ytest, c="r", s=5)
    Ridge_model=Ridge()
    Ridge_model.set_params(alpha=200)
    Ridge_model.fit(xtrain,ytrain)
    y_pre=Ridge_model.predict(x)
    plt.plot(x,y_pre,'r-')
# ARIMA模型
def arimaPre(ser):
    p,d,q=4,2,0
    nums=ser.values
    arima=ARIMA(endog=nums,order=(p,d,q))
    proArima = arima.fit(disp=-1)
    preValues=proArima.fittedvalues
    forest_n=20
    forest_nums=proArima.forecast(forest_n)
    print(forest_nums)
    fittedArima = preValues + 0
    fittedNums = fittedArima
    print(fittedNums)
    plt.plot(forest_nums[0])
    plt.plot(ser.diff().diff())
    plt.plot(nums, 'g-', lw=2, label=u'orignal')
    plt.plot(fittedNums, 'r-', lw=2, label=u'fitted')
    plt.legend(loc='best')
# 定义存储输入数据（x）和目标数据（y）的数组
x, y = [], []
df=pd.read_csv('data/groupsNumberPerCategory.csv').fillna(0)
ser=df['tech']
# arimaPre(ser)
# plt.show()
# y=df['tech'].values
# y2=df['dancing'].values
# x=range(0,len(y2))


cols=get_columns(df)
print(cols)
r_scores=[]
coefs=[]
ndf=pd.DataFrame({})
for item in cols[0:5]:
    tmp=train_and_predict_one_column(df[item],pre=True)
    coefs.append(tmp[0])
    r_scores.append(tmp[1])
    ys=tmp[2].reshape(1,-1)
    # print(np.rint(ys))
    ndf[item]=pd.Series(np.rint(ys[0]))
    # ndf=ndf.replace(range(-100,0),0)
    # RidgePredict(df[item])
print(ndf)
print(coefs)
print(r_scores)
# rd.to_csv_index(ndf,'data/predictGroupNumberPerCategory.csv')
plt.show()