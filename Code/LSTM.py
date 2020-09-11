import pandas as pd
import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from pandas import DataFrame
from pandas import concat
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import math
def parse(x):return pd.datetime.strptime(x, '%m/%d/%Y')
dataset = pd.read_csv('2000-2019Prices/MERGED_PRICES.csv', index_col=0, date_parser=parse)

"""
groups = [0, 1]
i = 1
plt.figure()
for group in groups:
	plt.subplot(len(groups), 1, i)
	plt.plot(values[:, group])
	plt.title(dataset.columns[group], y=0.5, loc='right')
	i += 1
plt.show()
"""
#print(dataset)

datadates = dataset.index.values
datamonths = pd.Series(data=[pd.to_datetime(x).month for x in datadates], index=datadates, name='month')
datadays = pd.Series([pd.to_datetime(x).day for x in datadates], index=datadates, name='day')
datamonths = datamonths.to_frame().join(datadays.to_frame())
dataset = datamonths.join(dataset)
values = dataset.values
values = values.astype('float32')
#print(dataset)
print(values)

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	"""
	Frame a time series as a supervised learning dataset.
	Arguments:
		data: Sequence of observations as a list or NumPy array.
		n_in: Number of lag observations as input (X).
		n_out: Number of observations as output (y).
		dropnan: Boolean whether or not to drop rows with NaN values.
	Returns:
		Pandas DataFrame of series framed for supervised learning.
    """
	n_vars = 1 if type(data) is list else data.shape[1]
	df = DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg


# frame as supervised learning
reframed = series_to_supervised(values, 12, 1)

# drop columns we don't want to predict (ie month, day, WTI on week t)
reframed.drop(reframed.columns[[48, 49, 50]], axis=1, inplace=True)

print("reframed head: ", reframed.head)

scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(reframed)

# split into train and test sets
values = scaled
n_train_weeks = 18 * 52
train = values[:n_train_weeks, :]
test = values[n_train_weeks:, :]
# split into input and outputs
train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]
# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

#print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

# design network
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')
# fit network
history = model.fit(train_X, train_y, epochs=10, batch_size=150, validation_data=(test_X, test_y), verbose=2,
                    shuffle=False)
"""
#plot history
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show()
"""

# make a prediction
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
# invert scaling for forecast
inv_yhat = np.concatenate((test_X[:, 0:], yhat), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:, -1]
# invert scaling for actual
test_y = test_y.reshape((len(test_y), 1))
inv_y = np.concatenate((test_X[:, 0:], test_y), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:, -1]
#for x, y in zip(inv_yhat, inv_y):
#	print("forecast: %.3f " % x, "actual: %.3f" % y)
plt.plot(inv_y, label = 'actual')
plt.plot(inv_yhat, label = 'forecast')
plt.legend()
plt.show()

# save to file for maybe implementing in flutter mobile app
keras_file = "gasPriceForcaster.h5"
model.save(keras_file)

# calculate RMSE
rmse = math.sqrt(mean_squared_error(inv_y, inv_yhat))

print('Test RMSE: %.3f' % rmse)