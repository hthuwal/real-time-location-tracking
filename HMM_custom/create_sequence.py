import pandas as pd
import os

# directory = "spencers/2018-1-1"

nas2ap = {
    2946: 0,
    3596: 1,
    3597: 2,
    3598: 3
}


def give_seq(directory, num_obs_per_seq):
    """
    Extract observation sequences from the log files.

    Where each observation is a dictionary with key = accesspoint, value = power

    Arguments:
        directory -- path to directory where log file is present
        num_obs_per_seq -- length of observation sequences

    Returns:
        ls_of_obs_seq -- List of observation sequences

    """
    data = None
    for nas in nas2ap:
        folder_path = os.path.join(directory, "NAS_%d" % (nas))

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            print(file_path)
            df = pd.read_json(file_path, lines=True)
            if data is None:
                data = df
            else:
                data = data.append(df)

    data['ts'] = pd.to_datetime(data['ts'], infer_datetime_format=True)
    most_freq_mac = data['mac'].value_counts().idxmax()

    data = data.loc[data['mac'] == most_freq_mac]
    data['ts'] = data['ts'].apply(lambda x: x.strftime('%H:%M'))

    data = data.groupby(['nasid', 'controllerid', 'position', 'ts', 'mac']).mean()
    data.reset_index(inplace=True)

    data = data.groupby(['controllerid', 'position', 'ts', 'mac'])
    lst = list(data)
    # df_loc_track = pd.DataFrame(columns=['conotrollerid', 'position', 'ts', 'mac', 'nasid', 'pwr', 'count'], dtype=object)
    observations = []
    for i in range(len(lst)):
        x = lst[i]

        cid_list = list(map(int, x[1]['nasid'].tolist()))
        pwr_list = list(map(float, x[1]['pwr'].tolist()))
        observations.append((x[0][2], cid_list, pwr_list))

    ls_of_obs_seq = []
    temp = []
    for i in range(len(observations)):
        if i != 0 and i % num_obs_per_seq == 0:
            ls_of_obs_seq.append(temp)
            temp = []

        obs = observations[i]
        cids = [nas2ap[c] for c in obs[1]]
        pwrs = obs[2]
        obs = {cid: pwr for cid, pwr in zip(cids, pwrs)}
        temp.append(obs)

        ls_of_obs_seq.append((temp, None))

    return ls_of_obs_seq


if __name__ == '__main__':
    hc = give_seq("../spencers/2018-1-1", 50)
