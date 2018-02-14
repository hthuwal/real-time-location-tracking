from __future__ import division
import pandas as pd
import datetime

macs = ["74:23:44:33:2f:b7", "00:0c:e7:4f:38:a5", "88:36:5f:f8:3b:4a", "84:38:38:f6:58:40", "c0:ee:fb:72:0c:27", "18:dc:56:8c:27:56", "80:58:f8:d8:ad:e1"]

df = pd.read_json("spencers_data/10.log", lines=True)  # reading data
df['ts'] = pd.to_datetime(df['ts'], infer_datetime_format=True)


df['ts'] = df['ts'].apply(lambda x: x + datetime.timedelta(hours=5, minutes=30))  # converrting utc time ist

df = df.loc[df['mac'].isin(macs)]  # filtering out data corresponding to our macs

# making code granular by per minute
df['ts'] = df['ts'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M'))
df = df.groupby(['nasid', 'controllerid', 'position', 'ts', 'mac']).mean()
df.reset_index(inplace=True)

