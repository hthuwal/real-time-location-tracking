import pandas as pd

# Readng path1 data and setting granularity to 1 min
df_path1 = pd.read_csv('../spencers_data/path1.csv')
df_path1['Start_time'] = pd.to_datetime(df_path1['Start_time'])
df_path1['Start_time'] = df_path1['Start_time'].apply(lambda x: x.strftime('%Y-%m-13 %H:%M:%S'))
df_path1['Start_time'] = pd.to_datetime(df_path1['Start_time'])

count = len(df_path1)
for index, row in df_path1.iterrows():
    if (row['Duration (min)'] == 2):
        df_path1.loc[index, 'Duration (min)'] = 1
        df_path1.loc[count, :] = df_path1.loc[index, :]
        df_path1.loc[count, 'Start_time'] = df_path1.loc[count, 'Start_time'] + pd.Timedelta('1 minute')
        count += 1

df_path1.sort_values('Start_time', inplace=True)
df_path1.reset_index(drop=True, inplace=True)
df_path1['Start_time'] = df_path1['Start_time'] + pd.Timedelta('12 hours')

# Reading path2 data and setting granularity to 1 min
df_path2 = pd.read_csv('../spencers_data/path2.csv')
df_path2['Start_time'] = pd.to_datetime(df_path2['Start_time'])
df_path2['Start_time'] = df_path2['Start_time'].apply(lambda x: x.strftime('%Y-%m-13 %H:%M:%S'))
df_path2['Start_time'] = pd.to_datetime(df_path2['Start_time'])

count = len(df_path2)
for index, row in df_path2.iterrows():
    if (row['Duration (min)'] == 2):
        df_path2.loc[index, 'Duration (min)'] = 1
        df_path2.loc[count, :] = df_path2.loc[index, :]
        df_path2.loc[count, 'Start_time'] = df_path2.loc[count, 'Start_time'] + pd.Timedelta('1 minute')
        count += 1

df_path2.sort_values('Start_time', inplace=True)
df_path2.reset_index(drop=True, inplace=True)
df_path2['Start_time'] = df_path2['Start_time'] + pd.Timedelta('12 hours')
