from __future__ import division
import pandas as pd
import os

f = os.listdir('logs')
f = [j for j in f if '2018' in j]

for file in f:
	df_day = pd.read_json('logs/'+file+'/0.log', lines=True)
	df_day['ts'] = pd.to_datetime(df_day['ts'], infer_datetime_format=True)
	for num in range(1, 24):
		df_hour = pd.read_json('logs/'+file+'/'+str(num)+'.log', lines=True)
		df_hour['ts'] = pd.to_datetime(df_hour['ts'], infer_datetime_format=True)
		df_day = df_day.append(df_hour, ignore_index=True)

	df_day.reset_index(inplace=True)
	del df_day['index']	

	df1 = df_day.groupby('mac')
	df1 = df1.count()
	df1.sort_values('nasid', inplace=True, ascending=False)
	mac = df1.index[0]
	count_probes = df1.loc[mac, 'nasid']
	total_probes = len(df_day)

	print file + ', mac - ' + str(mac) + ', count_probes - ' + str(count_probes) + ', total_probes - ' + str(total_probes) + ', %tage - ' + str(count_probes*100/total_probes)
