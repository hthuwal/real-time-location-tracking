import numpy as np
from scipy.stats import multivariate_normal as mvg
from tqdm import tqdm


class hmm(object):
    def __init__(self, states):
        self.random_state = np.random.RandomState(0)
        self.num_states = len(states)
        self.states = states
        self.starting_probs = self._normalize(self.random_state.rand(self.num_states))
        self.transition = ([0, 0, 0, 0], 1)  # initialized with mean 0, identitiy covariance matrix
        self.emission = [([0, 0, 0], 1)] * 4

    def _normalize(self, x):
        return (x + (x == 0)) / np.sum(x)

    def transition_func(self, i, j):
        """ Multivariate Gaussian Distribution of four variables """
        x1, y1 = self.states[i]
        x2, y2 = self.states[j]
        return mvg.pdf([x1, y1, x2, y2], mean=self.transition[0], cov=self.transition[1])

    def emission_func(self, i, obs, ap):
        """ Multivariate Gaussian Distribution of three variables for each AP """
        """ Could Try Gaussian Mixture Model """
        x1, y1 = self.states[i]
        return mvg.pdf([x1, y1, obs], mean=self.emission[ap][0], cov=self.emission[ap][1])

    def viterbi_dp(self, observed_seq):
        deltas = [[(0, None) for j in range(len(observed_seq))] for i in range(self.num_states)]
        for i in range(self.num_states):
            deltas[i][0] = (self.starting_probs[i], None)

        for j in range(1, len(observed_seq)):
            for i in range(self.num_states):
                temp = [self.transition_func(k, i) * deltas[k][j - 1][0] for k in range(self.num_states)]
                best = max(temp)  # todo multiply with emission probabilities based on observed data
                observation = observed_seq[j]
                for ap in observation:
                    best *= self.emission_func(i, observation[ap], ap)
                deltas[i][j] = (best, np.argmax(temp))

        deltas = np.array(deltas)
        winner = np.argmax(deltas[:, -1, 0])
        path = []
        for j in range(len(observed_seq) - 1, -1, -1):
            path.append(winner)
            winner = deltas[winner][j][1]
        return path

    def maximization(self, data):
        print("maximization")
        # data -  a list of (observation_seq, labels)
        # TODO check correctness
        state_data = []
        emission_data = {0: [], 1: [], 2: [], 3: []}
        start_probs = [1 for i in range(self.num_states)]
        for obs_seq, state_seq in data:
            start_probs[state_seq[0]] += 1
            for i in range(len(state_seq) - 1):
                state_data.append([self.states[i][0], self.states[i][1], self.states[i + 1][0], self.states[i + 1][1]])
                obs = obs_seq[i]
                for ap in obs:
                    emission_data[ap].append([self.states[i][0], self.states[i][1], obs[ap]])

            i = len(state_seq) - 1
            obs = obs_seq[i]
            for ap in obs:
                emission_data[ap].append([self.states[i][0], self.states[i][1], obs[ap]])

        self.transition = (np.mean(state_data, axis=0), np.cov(state_data, rowvar=False))

        for ap in emission_data:
            if len(emission_data[ap]) != 0:
                self.emission[ap] = (np.mean(emission_data[ap], axis=0), np.cov(emission_data[ap], rowvar=False))

        self.starting_probs = np.array(start_probs) / np.sum(np.array(start_probs))

    def expectation(self, data):
        # data -  a list of (observation_seq, labels) labels = None if not known
        print("Expectation")
        for i in tqdm(range(len(data))):
            data[i] = (data[i][0], self.viterbi_dp(data[i][0]))

    def em(self, data, max_iter=100):
        for i in range(max_iter):
            print("Step %d" % (i))
            self.expectation(data)
            self.maximization(data)


if __name__ == '__main__':
    test = hmm([(0, 0), (1, 0), (0, 1), (1, 1)])
