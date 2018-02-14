from __future__ import division
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import utility
import descartes

macs = ["74:23:44:33:2f:b7", "00:0c:e7:4f:38:a5", "88:36:5f:f8:3b:4a", "84:38:38:f6:58:40", "c0:ee:fb:72:0c:27", "18:dc:56:8c:27:56", "80:58:f8:d8:ad:e1"]
macs = ["c0:ee:fb:72:0c:27"]

aps = {
    1: (-22, 1),
    2: (0, 1),
    3: (0, 24),
    4: (-22, 26)
}


fig = plt.figure(1)


def plot_circles(circles, mac, ts):
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(mac + '\n' + str(ts))
    ax.set_xlim(-50, 35)
    ax.set_ylim(-10, 50)
    for circle in circles:
        print(circle)
        c = plt.Circle(circle[0], circle[1], color='b', fill=False)
        ax.add_artist(c)
    plt.pause(2)


def plot_polygon(p, mac, ts):
    
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(mac + '\n' + str(ts) + '\n' + str(p.centroid))
    ax.set_xlim(-50, 35)
    ax.set_ylim(-10, 50)
    ax.add_patch(descartes.PolygonPatch(p, fc='b', ec='k', alpha=0.2))
    plt.pause(2)


df = pd.read_json("spencers_data/13.log", lines=True)  # reading data
df['ts'] = pd.to_datetime(df['ts'], infer_datetime_format=True)


df['ts'] = df['ts'].apply(lambda x: x + datetime.timedelta(hours=5, minutes=30))  # converrting utc time ist

df = df.loc[df['mac'].isin(macs)]  # filtering out data corresponding to our macs

# making code granular by per minute
df['ts'] = df['ts'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M'))
df = df.groupby(['nasid', 'controllerid', 'position', 'ts', 'mac']).mean()
df.reset_index(inplace=True)

df = df.groupby(['nasid', 'position', 'ts', 'mac'])
lst = list(df)
df_loc_track = pd.DataFrame(columns=['nasid', 'position', 'ts', 'mac', 'controllerid', 'pwr', 'count'], dtype=object)

for i in range(len(lst)):
    x = lst[i]

    cid_list = list(map(str, x[1]['controllerid'].tolist()))
    pwr_list = list(map(str, x[1]['pwr'].tolist()))

    df_loc_track.loc[i, :] = [x[0][0], x[0][1], x[0][2], x[0][3], " ".join(cid_list), " ".join(pwr_list), len(cid_list)]

df_loc_track.reset_index(inplace=True)

for index, row in df_loc_track.iterrows():
    controllers = list(map(int, row['controllerid'].split()))
    powers = list(map(float, row['pwr'].split()))
    ts = row['ts']

    circles = []
    for cid, power in zip(controllers, powers):
        radial_distance = utility.rssi_to_dis(power)
        circles.append((aps[cid], radial_distance))

    intersection = utility.find_intersetion(circles)
    print(ts, intersection.centroid)
    input()
    # print(utility.signal_strength_to_distance(row['si']))
plt.show()
