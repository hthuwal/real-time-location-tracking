import pandas as pd
import os
import numpy as np 
import datetime

df_device = pd.read_csv('micromax.csv')
df_device = df_device[df_device['count'] == 4]
df_device.reset_index(drop=True, inplace=True)
# df_device.astype({'controllerid' : np.object})

df_fingerprint = pd.read_csv('gen_csvs/fingerprint.csv')

df_device_new = pd.DataFrame(columns=['ts', 'controllerid', 'pwr', 'pred_loc', 'act_loc'])

for i in range(len(df_device)):
	# print df_device.loc[i, 'controllerid']
	df_device.loc[i, 'controllerid'] = df_device.loc[i, 'controllerid'][1:-1]
	lst = df_device.loc[i, 'controllerid'].split(', ')
	df_device_new.loc[i, 'controllerid'] = lst
	df_device_new.loc[i, 'pwr'] = df_device.loc[i, 'pwr'][1:-1].split(', ')
	df_device_new.loc[i, 'ts'] = df_device.loc[i, 'ts']

	df_device_new.loc[i, 'controllerid'] = map(int, df_device_new.loc[i, 'controllerid'])
	df_device_new.loc[i, 'pwr'] = map(float, df_device_new.loc[i, 'pwr'])

df_device_new['ts'] = pd.to_datetime(df_device_new['ts'], infer_datetime_format=True)
df_device_new['ts'] = df_device_new['ts'].apply(lambda x: x + datetime.timedelta(hours=5, minutes=30))  # converrting utc time ist
df_device_new['ts'] = df_device_new['ts'].apply(lambda x: x.strftime('%H:%M'))

# print df_device_new
# print df_fingerprint

for i in range(len(df_device_new)):
	obs_pwr = df_device_new.loc[i, 'pwr']
	obs_pwr = np.asarray(obs_pwr)
	dot_prods = np.zeros(len(df_fingerprint))
	for j in range(len(df_fingerprint)):
		fng_pwr = [df_fingerprint.loc[j, 'pwr'+str(k)] for k in range(1, 5)]
		fng_pwr = np.asarray(fng_pwr)
		# dot_prods[j] = np.sum(np.multiply(obs_pwr, fng_pwr))
		dot_prods[j] = np.dot(obs_pwr, fng_pwr)

	idx = np.argmin(dot_prods)
	idx1 = dot_prods.argsort()[:5][::-1]
	val1 = dot_prods[idx1]

	list = []
	for g in idx1:	
		x = df_fingerprint.loc[g, 'X']
		y = df_fingerprint.loc[g, 'Y']
		list.append([x, y])

	print val1
	print str(list[0]) + ', ' + str(list[1]) + ', ' + str(list[2]) + ', ' + str(list[3]) + ', ' + str(list[4])
	x = df_fingerprint.loc[idx, 'X']
	y = df_fingerprint.loc[idx, 'Y']
	df_device_new.loc[i, 'pred_loc'] = [x, y]

# print df_device_new

df_path1 = pd.read_csv('../spencers_data/path1.csv')
df_path1['Start_time'] = pd.to_datetime(df_path1['Start_time'], infer_datetime_format=True)
df_path1['Start_time'] = df_path1['Start_time'].apply(lambda x: x + datetime.timedelta(hours=12))
df_path1['Start_time'] = df_path1['Start_time'].apply(lambda x: x.strftime('%H:%M'))
print df_path1
df_device_new = df_device_new[df_device_new['ts'].isin(df_path1['Start_time'])]
df_device_new.reset_index(drop=True, inplace=True)
for i in range(len(df_device_new)):
	ts = df_device_new.loc[i, 'ts']
	slic = df_path1[df_path1['Start_time'] == ts]
	x = slic.loc[slic.index[0], 'X']
	y = slic.loc[slic.index[0], 'Y']

	df_device_new.loc[i, 'act_loc'] = [x, y]

print df_device_new	
df_device_new.to_csv('micromax_fing_pred.csv')