from __future__ import division
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import utility
import descartes
import os

macs = ["74:23:44:33:2f:b7", "00:0c:e7:4f:38:a5", "88:36:5f:f8:3b:4a", "84:38:38:f6:58:40", "c0:ee:fb:72:0c:27", "18:dc:56:8c:27:56", "80:58:f8:d8:ad:e1"]

# factor to convert to inches (doesn't have any effect on the nature of plots as everything is just scaled up)
factor = 1

aps = {
    1: (-22 * factor, 1 * factor),
    2: (0 * factor, 1 * factor),
    3: (0 * factor, 24 * factor),
    4: (-22 * factor, 26 * factor)
}


fig = plt.figure(1)
ax = fig.add_subplot(1, 1, 1)


def plot_circles(circles, mac, ts):
    ax.cla()
    ax.set_title(mac + '\n' + str(ts))
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    for circle in circles:
        print(circle)
        c = plt.Circle(circle[0], circle[1], color='b', fill=False)
        ax.add_artist(c)

def plot(ay, x, y, color='b'):
    ay.plot(x, y, marker='o', markersize=3, color=color)
    plt.pause(1)

def plot_polygon(p, mac, ts):

    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(mac + '\n' + str(ts) + '\n' + str(p.centroid))
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.add_patch(descartes.PolygonPatch(p, fc='b', ec='k', alpha=0.2))
    plt.pause(2)


f = os.listdir('spencers_data')
f.sort()


mac = macs[1]
for file in f:
    base, ext = os.path.splitext(file)
    if(ext == ".log"):
        print(file)
        df = pd.read_json("spencers_data/%s" % (file), lines=True)  # reading data
        df['ts'] = pd.to_datetime(df['ts'], infer_datetime_format=True)

        df['ts'] = df['ts'].apply(lambda x: x + datetime.timedelta(hours=5, minutes=30))  # converrting utc time ist

        df = df.loc[df['mac'].isin([mac])]  # filtering out data corresponding to our macs

        # making code granular by per minute
        df['ts'] = df['ts'].apply(lambda x: x.strftime('%H:%M'))
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
        # hc = open("Weighted_mean/%s.csv" % (mac), 'a')
        # hc = open("smallest_area/%s.csv" % (mac), 'a')
        x = [-22, 0, 0, -22]
        y = [1, 1, 24, 26]
        for index, row in df_loc_track.iterrows():
            print(row['ts'])

            if row['count'] >= 2:
                controllers = list(map(int, row['controllerid'].split()))
                powers = list(map(float, row['pwr'].split()))
                mac = row['mac']
                ts = row['ts']

                circles = []
                for cid, power in zip(controllers, powers):
                    radial_distance = utility.rssi_to_dis(power)
                    circles.append((aps[int(cid)], radial_distance))

                intersection = utility.fiwc(circles)
                plot_circles(circles, mac, ts)
                plot(ax, x + [intersection.x],y + [intersection.y], 'red')
                # if intersection == None:
                #     pass

                # else:
                # hc.write(str(ts) + "," + str(intersection.centroid.x) + "," + str(intersection.centroid.y) + "\n")
        # hc.close()
        # input()
        # fig.clf()
        # plot_circles(circles, mac, ts)

    # plt.show()
