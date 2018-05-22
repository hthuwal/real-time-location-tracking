import pandas as pd
import numpy as np
import os
import sys
from tqdm import tqdm

from utils import hmm

nas_dict = {1: '2946', 2: '3596', 3: '3597', 4: '3598'}

nas = 1
tmp = os.listdir('../spencers_data/2018-1-1/NAS_' + nas_dict[nas] + '/')
df = pd.read_json('../spencers_data/2018-1-1/NAS_' + nas_dict[nas] + '/' + tmp[0], lines=True)
df['ts'] = pd.to_datetime(df['ts'], infer_datetime_format=True)
for log_file in tmp[1:]:
    df_hour = pd.read_json('../spencers_data/2018-1-1/NAS_' + nas_dict[nas] + '/' + log_file, lines=True)
    df_hour['ts'] = pd.to_datetime(df_hour['ts'], infer_datetime_format=True)
    df = df.append(df_hour, ignore_index=True)
    print(str(log_file) + ' for nas ' + str(nas) + ' appended.')
df.reset_index(drop=True, inplace=True)
df['ts'] = df['ts'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
df['ts'] = pd.to_datetime(df['ts'], infer_datetime_format=True)
del df['nasid']
del df['position']
df_ts1s = df.groupby(['controllerid', 'ts', 'mac'])
df = df_ts1s.mean()
df.reset_index(inplace=True)
df['pwr'] = df['pwr'].astype('int64')
df.columns = ['cid' + str(nas), 'ts', 'mac', 'pwr' + str(nas)]
df_nas['cid' + str(nas)] = nas
print('df formatted.')
print(df)


for nas in range(2, 5):
    tmp = os.listdir('../spencers_data/2018-1-1/NAS_' + nas_dict[nas] + '/')
    df_nas = pd.read_json('../spencers_data/2018-1-1/NAS_' + nas_dict[nas] + '/' + tmp[0], lines=True)
    df_nas['ts'] = pd.to_datetime(df_nas['ts'], infer_datetime_format=True)
    for log_file in tmp[1:]:
        df_hour = pd.read_json('../spencers_data/2018-1-1/NAS_' + nas_dict[nas] + '/' + log_file, lines=True)
        df_hour['ts'] = pd.to_datetime(df_hour['ts'], infer_datetime_format=True)
        df_nas = df_nas.append(df_hour, ignore_index=True)
        print(str(log_file) + ' for nas ' + str(nas) + ' appended.')
    df_nas.reset_index(drop=True, inplace=True)
    df_nas['ts'] = df_nas['ts'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    df_nas['ts'] = pd.to_datetime(df_nas['ts'], infer_datetime_format=True)
    del df_nas['nasid']
    del df_nas['position']
    df_ts1s = df_nas.groupby(['controllerid', 'ts', 'mac'])
    df_nas = df_ts1s.mean()
    df_nas.reset_index(inplace=True)
    df_nas['pwr'] = df_nas['pwr'].astype('int64')
    df_nas.columns = ['cid' + str(nas), 'ts', 'mac', 'pwr' + str(nas)]
    df_nas['cid' + str(nas)] = nas
    print('df formatted.')
    df = pd.merge(df, df_nas, on=['ts', 'mac'], how='outer')
    print(df)

df1 = df.groupby('mac')
df1 = df1.count()
df1.reset_index(inplace=True)
df1.sort_values(['pwr'], inplace=True, ascending=False)
mac = df1.loc[0, 'mac']

df_slice = df[df['mac'] == mac]
df_slice.reset_index(drop=True, inplace=True)

df_slice['ts_diff'] = df_slice['ts'].shift(-1) - df_slice['ts']
df_slice.drop([0], inplace=True)
df_slice.reset_index(drop=True, inplace=True)

start = df_slice[df_slice['ts_diff'] > 1]
start = start.index

sequences = []
for i in tqdm(range(len(start[:-1]))):
    df_seq = df_slice.loc[start[i]:start[i + 1], :]
    seq = []
    for j in df_seq.index:
        obs = {}
        for nas in range(1, 5):
            power = df_seq.loc[j, 'pwr' + str(nas)]
            if (not np.isnan(power)):
                obs[nas - 1] = power
        seq.append(obs)
    sequences.append(seq)

sequences = (sequences, None)

hidden_states = {}
count = 0
for x in range(-46, 31):  # XRange
    for y in range(-10, 45):  # YRange
        hidden_states[count] = (x, y)
        count += 1
n_hidden_states = len(hidden_states)

hmm_imp = hmm(hidden_states)
hmm_imp.em(sequences)
