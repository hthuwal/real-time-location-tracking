## create_sequence.py

**give_seq**

	Extract observation sequences from the log files.

	Where each observation is a dictionary with key = accesspoint, value = power

	Arguments:
    directory -- path to directory where log file is present
    num_obs_per_seq -- length of observation sequences

	Returns:
    ls_of_obs_seq -- List of observation sequences


## utils.py: hmm class

Following Functions have been implemented:

- Viterbi Dp
- Expectation Maximization to learn optimum parameters
- Transition Function: Multivariate Gaussian Distribution of four variables
- Emission Function: Multivariate Gaussian Distribution of four variables


