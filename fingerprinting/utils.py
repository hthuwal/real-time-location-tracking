import numpy as np

def euclidean_distance(a, b):
	a = np.array(a)
	b = np.array(b)
	return np.linalg.norm(a-b)