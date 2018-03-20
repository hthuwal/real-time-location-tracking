from __future__ import division
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import utils
import descartes
import os
import numpy as np

factor = 1

aps = {
    1: (-22 * factor, 1 * factor),
    2: (0 * factor, 1 * factor),
    3: (0 * factor, 24 * factor),
    4: (-22 * factor, 26 * factor)
}


fig = plt.figure(1)
ax = fig.add_subplot(1, 1, 1)
ax.autoscale()

aps_plot, = ax.plot([-22, 0, 0, -22], [1, 1, 24, 26], marker='o', markersize=10, ls='')
validation, = ax.plot([], [], marker='o', markersize=3, color='g')
path, = ax.plot([], [], marker='+', markersize=3, color='red')

def update(obj, x, y):
    x_old = obj.get_xdata()
    y_old = obj.get_ydata()
    x_old = np.append(x_old, x)
    y_old = np.append(y_old, y)
    obj.set_data(x_old, y_old)
    plt.pause(0.2)

df_path1 = pd.read_csv("../spencers_data/path1.csv")
df_path1['Start_time'] = pd.to_datetime(df_path1['Start_time'], infer_datetime_format=True)
df_path1['Start_time'] = df_path1['Start_time'].apply(lambda x: x + datetime.timedelta(hours=12))
df_path1['Start_time'] = df_path1['Start_time'].apply(lambda x: x.strftime('%H:%M'))
df_path1 = df_path1[['X', 'Y', 'Start_time']].values
df_path1 = dict([ (x[2],(x[0], x[1])) for x in df_path1 ])

name = "Micromax"
target = "micromax_fing_pred.csv"
df = pd.read_csv(target)
df = df[['pred_loc','act_loc','ts']].values

df = dict([ (x[2],(list(map(float,(x[0].strip('[]').split(',')))))) for x in df ])
print(df_path1)

num_loc = 0
count = 0
for ts in df_path1:
    act_x, act_y = df_path1[ts]
    update(validation, [act_x], [act_y])
    if ts in df:
        pred_x, pred_y = df[ts]
        num_loc += 1
        update(path, [pred_x], [pred_y])
        ax.legend([path, validation], ["# points: %d\ntime: %s" % (num_loc, ts)])
    count += 1
    plt.savefig("plots/%s/%03d.png" % (name, count))
    ax.set_title("%s\nFingerprinting" % (name))
    plt.pause(0.02)

plt.show()
# ax.set_title("%s\nHeurisitic 3\nRMSQ: %f" % (name, utility.root_mean_square_error(dict_path2, test_dict)))
# plt.savefig(target + "/%03d.png" % (count + 1))
# plt.show()
