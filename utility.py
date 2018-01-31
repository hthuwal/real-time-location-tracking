import math
from sympy import Point, Circle, intersection
import matplotlib.pyplot as plt



def signal_strength_to_distance(signal, freq):
	"""
	
	Calculates the distance in meters, given the signal strength in decibels and frequency in Ghz
	
	Arguments:
		signal {float} -- [Signal strength in decibals]
	
	Keyword Arguments:
		freq {number} -- [frequency of the signal] (default: {2.4})
	"""
	distance = 10 ** ((27.55 + abs(signal) - (20 * math.log10(freq*1000)))/20.0)
	distance = distance * 3.28084 #converting into foot
	return distance

def intersection_of_three_circel(x1, y1, r1, x2, y2, r2, x3, y3, r3):
	
	# Todo handle edge cases if any
	c1 = Circle(Point(x1,y1), r1)
	c2 = Circle(Point(x2,y2), r2)
	c3 = Circle(Point(x3,y3), r3)
	ans = intersection(c1,c2,c3)
	if len(ans)!=0:
		ans = [(p.x, p.y) for p in ans]
		return ans
	else:
		return None
