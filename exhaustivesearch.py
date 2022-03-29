import sys
from itertools import permutations
from timeit import default_timer as timer


start = timer()     #starting the timer

Ncities = 10     #definding how many cities
data = []

#opening and reading the csv file
with open("european_cities.csv", "r") as file:
    cities = file.readline()
    cities = cities.split(";")

    for line in file:
        tall_rad = line.split(";")
        data.append(tall_rad[:Ncities])

data = data[:Ncities]

#finding ALL the possible routes: 6!, 10!
perm = list(permutations([i for i in range(Ncities)]))

#finding the element (number) with "allPosibilities"-index and
#finding the distance
route = []
def f(n):
    list = []
    tempRoute = []
    for i in range(0, len(data)):
        list.append(data[n[i-1]][n[i]])
        tempRoute.append(n[i])
    route.append(tempRoute)
    return list


#saving the values I have found
#running for the loop so many times to as many cities I should have
permOfDistance = []
for i in range(len(perm)):
    permOfDistance.append(f(perm[i]))


#finding the distance, making it from str to float
sumDistance = []
for i in range(len(permOfDistance)):
    for j in range(len(permOfDistance[i])):
        permOfDistance[i][j] = float(permOfDistance[i][j])
    sumDistance.append(sum(permOfDistance[i]))


#finding the shortest route
shortestDistanse = min(sumDistance)
index = sumDistance.index(shortestDistanse)
finalRoute = route[index]


#appendding the cities after fiding the shortest
routeCities = []
for i in finalRoute:
    routeCities.append(cities[i])


end = timer()       #ending the timer
print(f"Shortest distance in km: {shortestDistanse}")
print(f"Shortest route of cities: {routeCities}")
print(f"Time used: {end-start}")
