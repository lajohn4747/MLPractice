import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
import numpy as np
import random
import sys

validArgs = {"--numPoints" : 0, "--low" : 1, "--high" : 2, "--numCentroids" : 3, "--threshold" : 4}
centroids = {}
prevNum = set()
NUM_POINTS = 100
LO_VAL = -100.0
HIGH_VAL = 100.0
NUM_CENTROIDS = 3
THRESHOLD = 1

def RepresentsInt(s):
    try: 
        return int(s)
    except ValueError:
        sys.exit("Arg expects an int")

def RepresentsFloat(s):
    try: 
        return float(s)
    except ValueError:
        sys.exit("Arg expects an float")

def createRandomPoints(numPoints, rangeNum):
	allPointsX = []
	allPointsY = []
	(lo, high) = rangeNum
	if( not (isinstance(lo, float) and isinstance(high, float)) ):
		sys.exit("Make sure range points are floats")



	if(not isinstance(numPoints, int)):
		sys.exit("numPoints should be an int")
	
	for i in range(0,numPoints):
		allPointsX.append(random.uniform(lo, high))
		allPointsY.append(random.uniform(lo, high))

	return allPointsX, allPointsY

def assignCentroidsAndUpdate(allPointsX, allPointsY, centroids):
	pointColorList = []
	newCentroids = []
	newCentroidValuesX = [0] * len(centroids)
	newCentroidValuesY = [0] * len(centroids)
	newCentroidValuesCount = [0] * len(centroids)
	for point in range(NUM_POINTS):
		pointColor = 0
		minValue = float("inf")
		for key, value in centroids.items():
			dist = getCentroidDistance(value, (allPointsX[point], allPointsY[point]))
			if dist < minValue:
				minValue = dist
				pointColor = key
		newCentroidValuesCount[pointColor] += 1
		newCentroidValuesX[pointColor] += allPointsX[point]
		newCentroidValuesY[pointColor] += allPointsY[point]
		pointColorList.append(pointColor)

	for newC in range(len(newCentroidValuesX)):
		newCentroids.append((newCentroidValuesX[newC]/newCentroidValuesCount[newC], newCentroidValuesY[newC]/newCentroidValuesCount[newC]))

	return pointColorList, newCentroids

def getCentroidDistance(centroidPoint, point):
	return (point[0] - centroidPoint[0])**2 + (point[1] -centroidPoint[1])**2

def checkCentroids(centroids, newCentroids):
	numCentroidsFitted = 0
	for c in range(len(newCentroids)):
		dist = getCentroidDistance(centroids[c], newCentroids[c])
		if(dist <= 1):
			numCentroidsFitted += 1

	return numCentroidsFitted == len(newCentroids)

if __name__ == "__main__":
		value = -1
		for arg in sys.argv[1:]:
			if(value >= 0):
				if(value == 0):
					NUM_POINTS = RepresentsInt(arg)
				elif(value == 1):
					LO_VAL = RepresentsFloat(arg)
				elif(value == 2):
					HIGH_VAL = RepresentsFloat(arg)
				elif(value == 3):
					NUM_CENTROIDS = RepresentsInt(arg)
				elif(value == 4):
					THRESHOLD = RepresentsFloat(arg)
				value = -1
			else:
				if(arg not in validArgs):
					sys.exit("No " + arg + " exists in this function")
				else:
					value = validArgs[arg]

		if(NUM_POINTS <=  NUM_CENTROIDS):
			print(NUM_POINTS)
			sys.exit("Number of points cannot be less than number of centroids")
		if(LO_VAL >= HIGH_VAL):
			sys.exit("Make sure lowest value is less than highest value")
		if(THRESHOLD <= 0.1):
			sys.exit("Threshold is too low")

		pointsX, pointsY = createRandomPoints(NUM_POINTS, (LO_VAL, HIGH_VAL))
		finishedAlgo = False
		colors = cm.rainbow(np.linspace(0, 1, NUM_CENTROIDS))
		colorIterator = 0
		plt.ion()
		for i in range(NUM_CENTROIDS):
			rand = random.randint(0,NUM_POINTS-1)
			while(rand in prevNum):
				rand = random.randint(0,NUM_POINTS-1)
			centroids[colorIterator] = (pointsX[rand], pointsY[rand])
			prevNum.add(rand)
			colorIterator += 1

		while(not finishedAlgo):
			plt.pause(0.5)
			pointColorList, newCentroids = assignCentroidsAndUpdate(pointsX, pointsY, centroids)

			plt.clf()

			for point in range(NUM_POINTS):
				plt.scatter(pointsX[point], pointsY[point], color=colors[pointColorList[point]])

			for key, value in centroids.items():
				plt.scatter(value[0], value[1], color="black")
			plt.axis([LO_VAL-10, HIGH_VAL+10, LO_VAL-10, HIGH_VAL+10])
			plt.show()

			finishedAlgo = checkCentroids(centroids, newCentroids)

			for c in range(len(newCentroids)):
				centroids[c] = newCentroids[c]

		plt.ioff()
		plt.title("DONE")
		plt.show()