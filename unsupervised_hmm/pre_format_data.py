import pandas as pd 
import numpy as np 
import os

f = os.listdir('../spencers_data/training_day_logs/')
f = [j for j in f if '.log' in j]

df = pd.read_json('../spencers_data/training_day_logs/'+f[0], lines=True)
df['ts'] = pd.to_datetime(df['ts'], infer_datetime_format=True)
for log_file in f[1:]:
	df_hour = pd.read_json('../spencers_data/training_day_logs/'+log_file, lines=True)
	df_hour['ts'] = pd.to_datetime(df_hour['ts'], infer_datetime_format=True)
	df = df.append(df_hour, ignore_index=True)

df['ts']= df['ts'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
df['ts'] = pd.to_datetime(df['ts'], infer_datetime_format=True)
df_ts1s = df.groupby(['nasid', 'controllerid', 'position', 'ts', 'mac'])
df = df_ts1s.mean()
df.reset_index(inplace=True)

del df['nasid']
del df['position']
print df

df.to_csv('modified_training_day_log.csv')