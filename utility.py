import math
from shapely.geometry import Point
from shapely.ops import cascaded_union
from itertools import combinations

def find_intersetion(circles):
	cs = [ Point(c[0][0],c[0][1]).buffer(c[1]) for c in circles]
	intersections = [a.intersection(b) for a,b in combinations(cs, 2)]
	
	intersection = []
	for each in intersections:
		if each.area != 0:
			intersection.append(each)
			
	intersection = min(intersection, key=lambda x:x.area)
	ans = cs[0]
	for c in cs:
		ans = ans.intersection(c)

	if(ans.area == 0):
		return intersection

	return ans

def signal_strength_to_distance(signal, freq):
	"""
	
	Calculates the distance in meters, given the signal strength in decibels and frequency in Ghz
	
	Arguments:
		signal {float} -- [Signal strength in decibals]
	
	Keyword Arguments:
		freq {number} -- [frequency of the signal] (default: {2.4})
	"""
	distance = 10 ** ((27.55 + abs(signal) - (20 * math.log10(freq*1000)))/20.0)
	distance = distance * 39.3701 #converting into inches
	return distance/34

def rssi_to_dis(signal):
	n = 2.2
	return 10 ** ((-40.5-signal) / (10*n))

def convert_radial_horizontal(d, h):
	return math.sqrt(d*d - h*h) * (39.3701/34)
# def intersection_of_three_circles(c1, c2, c3):
	
# 	# Todo handle edge cases if any
# 	# print c1, c2, c3
# 	c1 = Circle(Point(c1[0],c1[1]), c1[2])
# 	c2 = Circle(Point(c2[0],c2[1]), c2[2])
# 	c3 = Circle(Point(c3[0],c3[1]), c3[2])
# 	ans = intersection(c1,c2,c3)
# 	if len(ans)!=0:
# 		ans = [(p.x, p.y) for p in ans]
# 		return ans
# 	else:
# 		return None
