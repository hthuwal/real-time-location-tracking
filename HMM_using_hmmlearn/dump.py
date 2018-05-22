df_arr = df.groupby(['mac', 'ts'])
df1 = df_arr.count()
print len(df1)
print len(df1[df1['pwr'] == 4])
print len(df1[df1['pwr'] == 3])
print len(df1[df1['pwr'] == 2])
print len(df1[df1['pwr'] == 1])

slc = df1[df1['pwr'] == 3]
print slc.index.levels

df2 = pd.DataFrame(columns=df.columns)
for i in range(len(slc.index.levels[0])):
	mac = slc.index.levels[0][i]
	ts = slc.index.levels[1][i]
	slicee = df[(df['mac'] == mac) & (df['ts'] == ts)]
	df2 = df2.append(slicee, ignore_index=True)

df2.sort_values(['mac', 'ts'], inplace=True)
df2.reset_index(inplace=True, drop=True)
print df2
print df2.groupby('mac').ts.apply(lambda x: x.diff().mean())

# df_loc_track = df_loc_track[df_loc_track['count'] >= 4]
# df_loc_track.reset_index(inplace=True, drop=True)
# df_loc_track.sort_values(['mac', 'ts'], inplace=True)

# print df_loc_track

# df_grp = df_loc_track.groupby(['mac'])
# df_grp = df_grp.count()
# df_grp.reset_index(inplace=True)
# df_grp.sort_values(['count'], inplace=True, ascending=False)
# print df_grp

# sbst = df_grp[df_grp['count']<=60]
# df_loc_track.drop(df_loc_track[df_loc_track['mac'] in sbst['mac']].index, inplace=True)
# df_loc_track.reset_index(inplace=True, drop=True)

# print df_loc_track