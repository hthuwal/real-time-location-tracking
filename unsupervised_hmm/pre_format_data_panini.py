import pandas as pd
import numpy as np
import os
import sys

nas_dict = {1: '2946', 2: '3596', 3: '3597', 4: '3598'}
cid = sys.argv[1]
nas = nas_dict[int(cid)]

f = os.listdir('../spencers_data/')
print(f)
n = [j for j in range(1, 16)]
days = ['2018-1-' + str(j) for j in n]
print(days)
f = [j for j in f if j in days]
print(f)
tmp = os.listdir('../spencers_data/2018-1-1/NAS_' + nas + '/')
df = pd.read_json('../spencers_data/2018-1-1/NAS_' + nas + '/' + tmp[0], lines=True)
df['ts'] = pd.to_datetime(df['ts'], infer_datetime_format=True)
for day in f:
    hours = os.listdir('../spencers_data/' + day + '/NAS_' + nas + '/')
    print(hours)
    hours = [j for j in hours if '.log' in j]
    print(hours)
    for log_file in hours:
        df_hour = pd.read_json('../spencers_data/' + day + '/NAS_' + nas + '/' + log_file, lines=True)
        df_hour['ts'] = pd.to_datetime(df_hour['ts'], infer_datetime_format=True)
        df = df.append(df_hour, ignore_index=True)
        print(str(log_file) + ' for day ' + str(day) + ' appended.')
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
df['ts'] = df['ts'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
df['ts'] = pd.to_datetime(df['ts'], infer_datetime_format=True)
df_ts1s = df.groupby(['nasid', 'controllerid', 'position', 'ts', 'mac'])
df = df_ts1s.mean()
df.reset_index(inplace=True)
df['pwr'] = df['pwr'].astype('int64')
print('df formatted.')
del df['nasid']
del df['position']
print(df)

df.to_csv('modified_log_controller_' + cid + '.csv')
