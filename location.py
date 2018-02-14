from __future__ import division
import pandas as pd

macs = ["74:23:44:33:2f:b7", "00:0c:e7:4f:38:a5", "88:36:5f:f8:3b:4a", "84:38:38:f6:58:40", "c0:ee:fb:72:0c:27", "18:dc:56:8c:27:56", "80:58:f8:d8:ad:e1"]

df = pd.read_json("spencers_data/10.log", lines=True)
df = df.loc[df['mac'].isin(macs)]
print(df)