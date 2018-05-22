import matplotlib.pyplot as plt
import pandas as pd
import datetime
# import utility
import os
import numpy as np
from pykalman import KalmanFilter

macs = ["00:0c:e7:4f:38:a5", "84:38:38:f6:58:40", "c0:ee:fb:72:0c:27", "18:dc:56:8c:27:56", "80:58:f8:d8:ad:e1"]
names = ["Micromax", "Samsung S5", "oneplus x", "Yureka", "Moto"]
# factor to convert to inches (doesn't have any effect on the nature of plots as everything is just scaled up)
factor = 1

aps = {
    1: np.asarray([-22 * factor, 1 * factor]),
    2: np.asarray([0 * factor, 1 * factor]),
    3: np.asarray([0 * factor, 24 * factor]),
    4: np.asarray([-22 * factor, 26 * factor])
}

def rssi_to_dis(signal, n=2.5):
    return (10 ** ((-40 - signal) / (10 * n))) * (39.3701)

def heuristic3(dist_arr):
    weights = 1/dist_arr
    norm = np.sqrt(np.sum(np.square(weights), axis=1))
    norm = norm.reshape((len(norm), 1))
    weights = np.divide(weights, norm)
    res = np.zeros((weights.shape[0], 2))
    for j in range(weights.shape[0]):
        for i in range(1, 5):
            res[j, :] += aps[i]*weights[j, i-1]
    return res

def rms(x, y, x_validation, y_validation):
    r1 = np.asarray(x_validation) - np.asarray(x)
    r2 = np.asarray(y_validation) - np.asarray(y)
    res = np.sqrt(np.mean(np.square(r1)+np.square(r2)))
    return res

def plot(x, y, vx, vy, folder):
    fig = plt.figure(1)
    ax = fig.add_subplot(1, 1, 1)
    for i in range(len(y)):
        ax.clear()
        ax.set_xlim(-50, 50)
        ax.set_ylim(-50, 50)
        aps_plot, = ax.plot([-22, 0, 0, -22], [1, 1, 24, 26], marker='o', markersize=10, ls='')
        ax.plot(x[0:i], y[0:i], marker='+', color='red')
        ax.plot(vx[0:i], vy[0:i], marker='o', color='green')
        plt.pause(0.2)
        plt.savefig(folder+str(i)+'.png')

    plt.show()
    ax.clear()


f = os.listdir('../spencers_data')
f.sort()

# reading and plotting validation data
df_path = pd.read_csv("../paper1/outputs_path1.csv")
df_path['Start_time'] = pd.to_datetime(df_path['Start_time'], infer_datetime_format=True)
# df_path['Start_time'] = df_path['Start_time'].apply(lambda x: x + datetime.timedelta(hours=12))  # todo write proper code
df_path['Start_time'] = df_path['Start_time'].apply(lambda x: x.strftime('%H:%M'))
x_validation = df_path['X'].tolist()
y_validation = df_path['Y'].tolist()
ts1 = df_path['Start_time'].tolist()

df_rms = pd.DataFrame(columns=['Device', 'Path_Exp', 'RMS'])
count = 0

pe_dict = {
    2.5 : '2_half',
    3 : '3',
    3.5 : '3_half',
    4 : '4'
}

for idx in range(5):
    for path_exp in [2.5, 3, 3.5, 4]:
        mac = macs[idx]
        name = names[idx]
        observations = []
        for file in f:
            base, ext = os.path.splitext(file)
            if(ext == ".log"):
                print(file)
                df = pd.read_json("../spencers_data/%s" % (file), lines=True)  # reading data
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
                    pwrs = [-500 for i in range(4)]
                    x = lst[i]
                    cid_list = list(map(str, x[1]['controllerid'].tolist()))
                    pwr_list = list(map(str, x[1]['pwr'].tolist()))
                    for c, p in zip(cid_list, pwr_list):
                        pwrs[int(c) - 1] = float(p)
                    pwrs = np.ma.masked_values(pwrs, -500)
                    observations.append((x[0][2], pwrs))

        # observation for path1
        observations = [each for each in observations if (each[0] >= "17:05" and each[0] <= "17:26") or (each[0] >= "18:31" and each[0] <= "18:48")]
        print(observations)
        # times, seq = list(zip(*observations))
        # print(times)
        # print(seq)
        # print(observations)
        obs_dist = []
        for i in range(len(observations)):
            obs_dist.append([rssi_to_dis(j, path_exp) for j in observations[i][1]])
        print(obs_dist)

        kf = KalmanFilter(initial_state_mean=obs_dist[0], n_dim_obs=4)  # taking the centroid of area as the mean
        print("Expectation Maximization for - "+str(obs_dist[0]))
        # print(seq)
        kf.em(obs_dist, n_iter=1000, em_vars=['transition_covariance', 'observation_covariance', 'transtion_matrix', 'observation_matrix'])
        print("Estimating Path")
        ans = kf.smooth(obs_dist)[0]
        print(ans)
        print("Plotting")
        ans = np.asarray(ans)
        # y, x = list(zip(*ans))
        # x, y = list(zip(*ans))
        coords = heuristic3(ans)
        print(coords)
        x = coords[:, 0].tolist()
        y = coords[:, 1].tolist()

        print(rms(x, y, x_validation, y_validation))
        df_rms.loc[count, :] = [name, path_exp, rms(x, y, x_validation, y_validation)]
        count += 1

        file = name+'/'+pe_dict[path_exp]+'/'
        if not os.path.exists('plots/'+file):
            os.makedirs('plots/'+file)
        plot(x, y, x_validation, y_validation, 'plots/'+file)

        df_rms.to_csv('rms_values.csv', index=False)

        # # for i in range(init_means.shape[0]):
        # kf = KalmanFilter(initial_state_mean=[0, 0], n_dim_obs=4)  # taking the centroid of area as the mean
        # print("Expectation Maximization for - ")
        # # print(seq)
        # kf.em(seq, n_iter=1000, em_vars=['transition_covariance', 'observation_covariance', 'transtion_matrix', 'observation_matrix'])
        # print("Estimating Path")
        # ans = kf.smooth(seq)[0]
        # print("Plotting")
        # y, x = list(zip(*ans))
        # # x, y = list(zip(*ans))

        # plot(x, y, x_validation, y_validation)
