import numpy as np 
import pandas as pd
import os
import sys
import timeit

from hmmlearn import hmm
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib

cid = sys.argv[1]

filename = 'model_'+cid+'.pkl'
model = joblib.load(open(filename), 'w')
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
    print(hidden_states)
    thefile = open('hidden_states_model_'+cid+'_device_'+names[i]+'.txt', 'w')
    thefile.write(list(map(hidden_states)))
    thefile.close()