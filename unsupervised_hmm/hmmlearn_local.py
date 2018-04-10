import numpy as np 
import pandas as pd
import os
import sys
import timeit

from hmmlearn import hmm
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib

start = timeit.default_timer()
np.random.seed(42)

cid = sys.argv[1]

df = pd.read_csv('modified_training_day_log.csv')
del df['Unnamed: 0']
df['pwr'] = df['pwr'].astype('int64')

macs = ["00:0c:e7:4f:38:a5", "84:38:38:f6:58:40", "c0:ee:fb:72:0c:27", "18:dc:56:8c:27:56", "80:58:f8:d8:ad:e1"]
names = ["Micromax", "Samsung S5", "oneplus x", "Yureka", "Moto"]

df = df[df['controllerid'] == int(cid)]
print(df['mac'].isin(macs))
df = df[np.invert(df['mac'].isin(macs))]

df.reset_index(inplace=True, drop=True)

grp = df.groupby(['mac'])
df1 = grp.count()
df1.sort_values(['pwr'], inplace=True, ascending=False)
macs = df1[df1['pwr']>=60].index
macs = macs.tolist()
df = df[df['mac'].isin(macs)]
df.reset_index(inplace=True, drop=True)
df.sort_values(['mac', 'ts'], inplace=True)
df.reset_index(inplace=True, drop=True)
print(df)

grp = df.groupby(['mac'])
lst = list(grp)
observed_sequences = []
observed_timestamps = []
len_samples = np.zeros(len(lst), dtype=int)
for i in range(len(lst)):
    x = lst[i]
    ts_list = np.asarray(x[1]['ts'])
    len_samples[i] = len(ts_list)
    pwr_list = np.zeros(len(x[1]['pwr'])+2, dtype=int)
    pwr_list[1:-1] = np.asarray(x[1]['pwr'])
    pwr_list[len(pwr_list)-1] = sys.maxsize
    observed_sequences.append(pwr_list)
    observed_timestamps.append(ts_list)

X = np.asarray(df['pwr'])
le = LabelEncoder()
le.fit(X)
print(le.classes_)
print(le.transform(X))
X_d = le.transform(X)
print(le.inverse_transform(X_d))
# X_d = np.asarray(list(map(int, X_d)))
X_d = X_d.reshape((len(X_d), 1))

#For the very moment we are creating a hidden state for every possible location within the shop. Later we can think of narrowing it down
hidden_states = {}
count = 0
for x in range(-46, 31): #XRange
	for y in range(-10, 45): #YRange
		hidden_states[count] = (x, y)
		count += 1
n_hidden_states = len(hidden_states)

# model = hmm.MultinomialHMM(n_components=n_hidden_states).fit(np.atleast_2d(X_d).T, len_samples)
print(len_samples)
print('Starting Training...')
model = hmm.MultinomialHMM(n_components=n_hidden_states).fit(X_d, len_samples)
print('Finished Training!')
model.monitor_
model.monitor_.converged
filename = 'model_'+cid+'.pkl'
joblib.dump(model, filename)
stop = timeit.default_timer()
print(stop-start)

df_test = pd.read_csv('modified_training_day_log.csv')
for i in range(len(macs)):
    df1 = df_test[(df_test['controllerid'] == int(cid)) & (df_test['mac'] == macs[i])]
    df1.reset_index(inplace=True, drop=True)
    X = np.asarray(df1['pwr'])
    X_d = le.transform(X)
    X_d = X_d.reshape((len(X_d), 1))
    hidden_states = model.predict(X_d)
    thefile = open('hidden_states_model_'+cid+'_device_'+names[i]+'.txt', 'w')
    thefile.write(list(map(hidden_states)))
    thefile.close()