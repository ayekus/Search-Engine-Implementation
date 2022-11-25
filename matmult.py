import math


def mult_matrix(a, b):
	if (len(a[0]) != len(b)):
		return None

	newMatrix = []
	total = 0
	#go through all of A's rows 
	for i in range(0, len(a)):
		newMatrix.append([])
		#go through all of B's columns for each of A's rows
		for j in range(0, len(b[0])):
			total = 0
			#go through all values in A's rows and B's columns, multiply them and then add them to total
			for k in range(0, len(b)):
				total += a[i][k] * b[k][j]
			newMatrix[i].append(total)
	return newMatrix

def euclidean_dist(a,b):
	if (len(a) != 1) or (len(b) != 1) or (len(a[0]) != len(b[0])):
		return None

	distance = 0
	totalDistance = 0
	for i in range (0, len(a[0])):
		distance = 0
		distance = (a[0][i] - b[0][i])**2
		totalDistance += distance
	totalDistance = math.sqrt(totalDistance) 
	return totalDistance