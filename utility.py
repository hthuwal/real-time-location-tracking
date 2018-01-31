import math

def signal_strength_to_distance(signal, freq):
	"""
	
	Calculates the distance in meters, given the signal strength in decibels and frequency in Ghz
	
	Arguments:
		signal {float} -- [Signal strength in decibals]
	
	Keyword Arguments:
		freq {number} -- [frequency of the signal] (default: {2.4})
	"""
	distance = 10 ** ((27.55 + abs(signal) - (20 * math.log10(freq*1000)))/20.0)
	return distance
