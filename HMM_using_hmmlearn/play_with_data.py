import pandas as pd 
import numpy as np 
import os
import sys

df = pd.read_csv('modified_training_day_log.csv')
del df['Unnamed: 0']

df = df[df['controllerid'] == 1]
df.reset_index(inplace=True, drop=True)
df['pwr'] = df['pwr'].astype('int64')

grp = df.groupby(['mac'])
df1 = grp.count()
df1.sort_values(['pwr'], inplace=True, ascending=False)
macs = df1[df1['pwr']>=60].index
macs = macs.tolist()
df = df[df['mac'].isin(macs)]
df.reset_index(inplace=True, drop=True)
df.sort_values(['mac', 'ts'], inplace=True)
df.reset_index(inplace=True, drop=True)
print df

grp = df.groupby(['mac'])
lst = list(grp)
observed_sequences = []
observed_timestamps = []
for i in range(len(lst)):
    x = lst[i]
    ts_list = np.asarray(x[1]['ts'])
    pwr_list = np.zeros(len(x[1]['pwr'])+2, dtype=int)
    pwr_list[1:-1] = np.asarray(x[1]['pwr'])
    pwr_list[len(pwr_list)] = sys.maxint
    observed_sequences.append(pwr_list)
    observed_timestamps.append(ts_list)

#Training - Forward-Backward Algorithm

#Create Latent States
#For the very moment we are creating a hidden state for every possible location within the shop. Later we can think of narrowing it down
hidden_states = {}
count = 0
for x in range(-46, 31): #XRange
	for y in range(-10, 45): #YRange
		hidden_states[count] = (x, y)
		count += 1
n_hidden_states = len(hidden_states)

observed_states_vals = df['pwr'].unique()
observed_states_vals = np.sort(observed_states_vals)
observed_states = {}
# count = 1
for i in range(len(observed_states_vals)):
	observed_states[observed_states_vals[i]] = i
	# count += 1
n_observed_states = len(observed_states)

#Initialisation of States
#Matrix storing the probabilities of transitioning from one matrix, to another
transition_mat = np.random.uniform(size=n_hidden_states*n_hidden_states).reshape((n_hidden_states, n_hidden_states))
norm_denom = np.sqrt(np.sum(transition_mat, axis=1))
transition_mat = (transition_mat.T/norm_denom).T #Normalisation

#Array storing the probabilities of a given hidden state being the starting one
start_arr = np.random.uniform(size=n_hidden_states)
norm_denom = np.sqrt(np.sum(start_arr))
start_arr = (start_arr/norm_denom) #Normalisation

#Array storing the probabilities of a given hidden state being the finishing one
finish_arr = np.random.uniform(size=n_hidden_states)
norm_denom = np.sqrt(np.sum(finish_arr))
finish_arr = (finish_arr/norm_denom) #Normalisation

#Matrix storing the probabilities of emission of observed state, given a particular hidden state
emission_mat = np.random.uniform(size=n_observed_states*n_hidden_states).reshape((n_hidden_states, n_observed_states))
norm_denom = np.sqrt(np.sum(emission_mat, axis=1))
emission_mat = (emission_mat.T/norm_denom).T #Normalisation

while not convergence:
	for obs in observed_sequences:
		seq_len = len(obs[-1:1])

		beta = np.zeros(seq_len, n_hidden_states)
		for i in range(seq_len-1, 0, -1):
			if (i == (seq_len-1)):
				beta[i, :] = finish_arr
			idx = observed_states[obs[i+1]]
			tmp = np.multiply(emission_mat[:, idx], beta[i+1, :])
			beta[i, :] = np.sum(np.divide(transition_mat, tmp), axis=1).T

		#Review Alpha Code
		alpha = np.zeros(seq_len, n_hidden_states)
		for i in range(seq_len):
			if (i == 0):
				alpha[i, :] = start_arr
			idx = observed_states[obs[i]]
			tmp = np.multiply(emission_mat[:, idx], alpha[i-1, :])
			alpha[i, :] = np.sum(np.divide(transition_mat, tmp), axis=1).T

		
		