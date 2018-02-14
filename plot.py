import matplotlib.pyplot as plt
import pandas as pd
import descartes
import datetime

fig = plt.figure(1)
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)


def plot(ay, x, y, color='b'):
    ay.set_xlim(-50, 35)
    ay.set_ylim(-10, 50)
    ay.plot(x, y, marker='o', markersize=3, color=color)
    plt.pause(0.2)

# def plot_result()


# reading and plotting validation data
validation_data1 = pd.read_csv("spencers_data/path1.csv")
validation_data1['Start_time'] = pd.to_datetime(validation_data1['Start_time'], infer_datetime_format=True)
validation_data1['Start_time'] = validation_data1['Start_time'].apply(lambda x: x + datetime.timedelta(hours=12))  # todo write proper code
validation_data1['Start_time'] = validation_data1['Start_time'].apply(lambda x: x.strftime('%H:%M'))
x_validation1 = validation_data1['X'].tolist()
y_validation1 = validation_data1['Y'].tolist()
ts1 = validation_data1['Start_time'].tolist()
plot(ax1, x_validation1, y_validation1)
plot(ax2, x_validation1, y_validation1)

validation_data2 = pd.read_csv("spencers_data/path2.csv")
validation_data2['Start_time'] = pd.to_datetime(validation_data2['Start_time'], infer_datetime_format=True)
validation_data2['Start_time'] = validation_data2['Start_time'].apply(lambda x: x + datetime.timedelta(hours=12))  # todo write proper code
validation_data2['Start_time'] = validation_data2['Start_time'].apply(lambda x: x.strftime('%H:%M'))
x_validation2 = validation_data2['X'].tolist()
y_validation2 = validation_data2['Y'].tolist()
ts2 = validation_data2['Start_time'].tolist()
plot(ax1, x_validation2, y_validation2)
plot(ax2, x_validation2, y_validation2)

macs = ["74:23:44:33:2f:b7", "00:0c:e7:4f:38:a5", "88:36:5f:f8:3b:4a", "84:38:38:f6:58:40", "c0:ee:fb:72:0c:27", "18:dc:56:8c:27:56", "80:58:f8:d8:ad:e1"]
mac = macs[5]

# reading and plotting heuristic1
test_data1 = pd.read_csv("smallest_area/%s.csv" % mac, header=None)
test_data1 = test_data1.loc[test_data1[0].isin(ts1)]
x_test1 = test_data1[1].tolist()
y_test1 = test_data1[2].tolist()
ts = test_data1[0].tolist()
for i in range(len(x_test1)):
    print(x_test1[:i + 1])
    plot(ax1, x_test1[:i + 1], y_test1[:i + 1], color='r')

plot(ax1, x_test1, y_test1, color='r')

# reading and plotting heuristic1
# test_data2 = pd.read_csv("smallest_area/%s.csv" % mac, header=None)
# test_data2 = test_data2.loc[test_data2[0].isin(ts1+ts2)]
# x_test2 = test_data2[1].tolist()
# y_test2 = test_data2[2].tolist()
# ts = test_data2[0].tolist()
# plot(ax2, x_test2, y_test2, color='r')
plt.show()
