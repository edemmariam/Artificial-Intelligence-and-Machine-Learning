from timeit import default_timer as timer
from itertools import permutations
import numpy as np
import copy
import statistics



start = timer()     #starting the timer

Ncities = 24      #definding how many cities

#opening and reading the csv file
data = []
with open("european_cities.csv", "r") as file:
    cities = file.readline()
    cities = cities.split(";")

    for line in file:
        tall_rad = line.split(";")
        data.append(tall_rad[:Ncities])

#making it from str to float
data = data[:Ncities]
for i in range(len(data)):
    for j in range(len(data[i])):
        data[i][j] = float(data[i][j])


#finding the neighbors to a random route. I am keeping the first
#element of that route fixed, such that I find the neightbors
#with the same starting-index
def neighbors(numbers):
    startRoutes = []
    distance = []
    for i in range(1, len(numbers)-1):
        for j in range(i + 1, len(numbers)):
            numbersCopy = copy.deepcopy(numbers)
            temp = numbersCopy[i]
            numbersCopy[i] = numbersCopy[j]
            numbersCopy[j] = temp
            startRoutes.append(numbersCopy)

    for i in range(len(startRoutes)):
        distance.append(findingRoute(startRoutes[i]))
    return startRoutes, distance


#converting the route with number to the distance
def findingRoute(n):
    distanceRoutes = []
    for i in range(0, len(data)):
        distanceRoutes.append(data[n[i-1]][n[i]])
    sumDistaceRoutes = sum(distanceRoutes)
    return sumDistaceRoutes


#using a def function to later run the while-loop n times
#ti find the best result. I run it 20 times such that the
#code does not stuck on local optimum
def min_idx():
    numbers = np.arange(Ncities)
    np.random.shuffle(numbers)
    SR, D = neighbors(numbers)

    minimum = min(D)
    index = D.index(minimum)
    routes = SR[index]

    shortest  = 100000
    while minimum < shortest:
        shortest = minimum
        SR, D = neighbors(routes)
        minimum = min(D)
        index = D.index(minimum)
        indexRoutes = SR[index]
    return minimum, indexRoutes


#running the code 20 times and appending to a list
bestDistances = []
routes = []
for i in range(20):
    a, b = min_idx()
    bestDistances.append(a)
    routes.append(b)


#finding min and max route
shortestRoute = min(bestDistances)
longestRoute = max(bestDistances)

#finding the index of the best and worst routes
indexShort = bestDistances.index(shortestRoute)
finalRouteShort = routes[indexShort]

indexLong = bestDistances.index(longestRoute)
finalRouteLong = routes[indexLong]


#appendding the cities after fiding the shortest and longest
routeCitiesShort = []
for i in finalRouteShort:
    routeCitiesShort.append(cities[i])

routeCitiesLong = []
for i in finalRouteLong:
    routeCitiesLong.append(cities[i])




end = timer()       #ending the timer
print(f"Shortest distance in km: {shortestRoute}")
print(f"Shortest route of cities: {routeCitiesShort}")
print(f"Longest distance in km: {longestRoute}")
print(f"Longest route of cities: {routeCitiesLong}")
print(f"Time used: {end-start}")
print(f"stdev: {statistics.stdev(bestDistances)}")
print(f"mean: {statistics.mean(bestDistances)}")
