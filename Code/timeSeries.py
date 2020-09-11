import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

df = pd.read_csv('2000-2019Prices/MERGED_PRICES - Copy.csv', parse_dates = ['Date'], index_col = ['Date'])
df.head()
plt.xlabel('Date')
plt.ylabel('Price')
plt.plot(df)
#plt.show()

def get_stationarity(timeseries):
    
    # rolling statistics
    rolling_mean = timeseries.rolling(window=12).mean()
    rolling_std = timeseries.rolling(window=12).std()
    
    # rolling statistics plot
    plt.plot(df, color = 'blue', label = 'Original')
    plt.plot(rolling_mean, color = 'red', label = 'Rolling Mean')
    plt.plot(rolling_std, color = 'black', label = 'Rolling Std')
    plt.legend(loc = 'best')
    plt.title('Rolling Mean & Rolling Standard Deviation')
    plt.show()
    
    # Dickey–Fuller test:
    result = adfuller(timeseries['WTI Price'])
    print('ADF Statistic: {}'.format(result[0]))
    print('p-value: {}'.format(result[1]))
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t{}: {}'.format(key, value))

df_log = np.log(df)
plt.plot(df_log)

rolling_mean_exp_decay = df_log.ewm(halflife=12, min_periods=0, adjust=True).mean()
df_log_exp_decay = df_log - rolling_mean_exp_decay
df_log_exp_decay.dropna(inplace=True)
#get_stationarity(df_log_exp_decay)


decomposition = seasonal_decompose(df_log_exp_decay) 
model = ARIMA(df_log_exp_decay, order=(2,1,2))
results = model.fit(disp=-1)
plt.plot(df_log_exp_decay)
plt.plot(results.fittedvalues, color='red')
plt.show()