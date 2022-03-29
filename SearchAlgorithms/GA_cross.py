import sys
from itertools import permutations
from timeit import default_timer as timer
import numpy as np
import copy
import random
import matplotlib.pyplot as plt
import statistics

Ncities = 24

data = []
cities = []
with open("./european_cities.csv", "r") as file:
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

def randomRoutes():
    population = []
    for i in range(p):
        numbers = list(range(Ncities))
        np.random.shuffle(numbers)
        population.append(numbers)
    return population

#converting the route with number to the distance
def findingRoute(n, data):
    distanceRoutes = []
    for i in range(0, len(data)):
        distanceRoutes.append(data[n[i-1]][n[i]])
    sumDistaceRoutes = sum(distanceRoutes)
    return sumDistaceRoutes

#finding the reverse score, because the lowest
#value needs a higher score to be choosen
def giveScore(sumDistance):
    temp = []
    for i in range(len(sumDistance)):
        A2 = 1/sumDistance[i]
        temp.append(A2)
    S = []
    for i in range(len(temp)):
        S.append(temp[i]/sum(temp))
    return S



#using partially mapped crossover to change the routes
def pmx(parent1, parent2, start, stop):
    child = [None]*len(parent1)

    child[start:stop] = parent1[start:stop]

    for index, i in enumerate(parent2[start:stop]):
        index += start
        if i not in child:
            while child[index] != None:
                index = parent2.index(parent1[index])
            child[index] = i

    for index, i in enumerate(child):
        if i == None:
            child[index] = parent2[index]
    return child

def pmx_pair(parent1, parent2):
    half = len(parent1) // 2
    start = np.random.randint(0, len(parent1) - half)
    stop = start + half
    return pmx(parent1, parent2, start, stop)

def survivors(population, populationDistance):
    newPopulation = []
    tempScore = sorted(populationDistance)[:p]
    scoreIndex = []
    for i in range(len(tempScore)):
        scoreIndex.append(populationDistance.index(tempScore[i]))
    for i in range(len(scoreIndex)):
        newPopulation.append(population[scoreIndex[i]])
    return newPopulation, sum(tempScore[0:5])/len(tempScore[0:5])


def main(Ncities, p, o):

    generations = 1
    start = timer()
    population = randomRoutes()

    averageDistOfBest = []

    #finding the sum of distance of the population
    populationDistance = []
    for i in range(len(population)):
        populationDistance.append(findingRoute(population[i], data))

    score = giveScore(populationDistance)


    parentsIndex = (np.random.choice(len(population), size=o, replace=False, p=score))

    #appending the parents based of the index that np.random.choice chose
    #with respect to population-probability
    parents = []
    for i in range(len(parentsIndex)):
        parents.append(population[parentsIndex[i]])

    #giving pmx() function parent #1 and parent #2 and
    #appendding the offsprings to a list
    offspring = []
    for i in range(len(parents)):
        offspring.append(pmx_pair(parents[i-1], parents[i]))

    #finding the distance of the offsrping
    offspringDistance = []
    for i in range(len(offspring)):
        offspringDistance.append(findingRoute(offspring[i], data))

    #I use the distance above to give the offspring score
    scoreOffsprings = giveScore(offspringDistance)

    #I append the offsprings to the original population-list to run
    #the program n times, where n is the number of generations
    for i in range(len(scoreOffsprings)):
        population.append(offspring[i])
        score.append(scoreOffsprings[i])

    #finding this time the distance of the population, (populatoin and offspring)
    populationDistance = []

    for i in range(len(population)):
        populationDistance.append(findingRoute(population[i], data))

    population, bestDist = survivors(population, populationDistance)
    averageDistOfBest.append(bestDist)

    populationDistance = []
    for i in range(len(population)):
        populationDistance.append(findingRoute(population[i], data))
    score = giveScore(populationDistance)

    improvementCheckDist = min(populationDistance)
    noImprovement = 0
    while noImprovement < 50:
        parentsIndex = (np.random.choice(len(population), size=o, replace=False, p=score))

        parents = []
        for i in range(len(parentsIndex)):
            parents.append(population[parentsIndex[i]])

        offspring = []
        for i in range(len(parents)):
            offspring.append(pmx_pair(parents[i-1], parents[i]))

        offspringDistance = []
        for i in range(len(offspring)):
            offspringDistance.append(findingRoute(offspring[i], data))

        scoreOffsprings = giveScore(offspringDistance)

        for i in range(len(scoreOffsprings)):
            population.append(offspring[i])
            score.append(scoreOffsprings[i])

        populationDistance = []
        for i in range(len(population)):
            populationDistance.append(findingRoute(population[i], data))

        population, bestDist = survivors(population, populationDistance)
        averageDistOfBest.append(bestDist)

        populationDistance = []
        for i in range(len(population)):
            populationDistance.append(findingRoute(population[i], data))
        score = giveScore(populationDistance)

        if improvementCheckDist <= min(populationDistance):
            noImprovement += 1
        else:
            improvementCheckDist = min(populationDistance)
        generations += 1
    end = timer()
    return population, populationDistance, generations, averageDistOfBest, end-start



p = 100
o = 50
n = 1

averageDistOfBest = []

population = []
populationDistance = []
generations = []
time = []
for i in range(n):
    pop, dist, gen, bestDist, t = main(Ncities, p, o)
    population.append(pop)
    populationDistance.append(dist)
    generations.append(gen)
    averageDistOfBest.append(bestDist)
    time.append(t)


shortest = min(populationDistance[0])
longest = max(populationDistance[0])
standardDiv = statistics.stdev(populationDistance[0])
meanDist = statistics.mean(populationDistance[0])
#finding the index of the cities from the origival csv file
indexB = populationDistance[0].index(shortest)
finalB = population[0][indexB]

indexW = populationDistance[0].index(longest)
finalW = population[0][indexW]
#appendding the cities after fiding the shortest and longest route
best = []
for i in finalB:
    best.append(cities[i])

worst = []
for i in finalW:
    worst.append(cities[i])

print(f"results with population of {p} and offsprings of {o}")
print(f"Shortest distance in km: {shortest}")
print(f"The city route: {best}")
print(f"Longest route of cities: {longest}")
print(f"The city route: {worst}")
print(f"Standard Deviation: {standardDiv}")
print(f"Mean Distance: {meanDist}")
print(f"Time used: {time}")
print()

p = 200
o = 160

population = []
populationDistance = []
generations = []
time = []
for i in range(n):
    pop, dist, gen, bestDist, t = main(Ncities, p, o)
    population.append(pop)
    populationDistance.append(dist)
    generations.append(gen)
    averageDistOfBest.append(bestDist)
    time.append(t)


shortest = min(populationDistance[0])
longest = max(populationDistance[0])
standardDiv = statistics.stdev(populationDistance[0])
meanDist = statistics.mean(populationDistance[0])
#finding the index of the cities from the origival csv file
indexB = populationDistance[0].index(shortest)
finalB = population[0][indexB]

indexW = populationDistance[0].index(longest)
finalW = population[0][indexW]
#appendding the cities after fiding the shortest and longest route
best = []
for i in finalB:
    best.append(cities[i])

worst = []
for i in finalW:
    worst.append(cities[i])

print(f"results with population of {p} and offsprings of {o}")
print(f"Shortest distance in km: {shortest}")
print(f"The city route: {best}")
print(f"Longest route of cities: {longest}")
print(f"The city route: {worst}")
print(f"Standard Deviation: {standardDiv}")
print(f"Mean Distance: {meanDist}")
print(f"Time used: {time}")
print()

p = 500
o = 250

population = []
populationDistance = []
generations = []
time = []
for i in range(n):
    pop, dist, gen, bestDist, t = main(Ncities, p, o)
    population.append(pop)
    populationDistance.append(dist)
    generations.append(gen)
    averageDistOfBest.append(bestDist)
    time.append(t)


shortest = min(populationDistance[0])
longest = max(populationDistance[0])
standardDiv = statistics.stdev(populationDistance[0])
meanDist = statistics.mean(populationDistance[0])
#finding the index of the cities from the origival csv file
indexB = populationDistance[0].index(shortest)
finalB = population[0][indexB]

indexW = populationDistance[0].index(longest)
finalW = population[0][indexW]
#appendding the cities after fiding the shortest and longest route
best = []
for i in finalB:
    best.append(cities[i])

worst = []
for i in finalW:
    worst.append(cities[i])

print(f"results with population of {p} and offsprings of {o}")
print(f"Shortest distance in km: {shortest}")
print(f"The city route: {best}")
print(f"Longest route of cities: {longest}")
print(f"The city route: {worst}")
print(f"Standard Deviation: {standardDiv}")
print(f"Mean Distance: {meanDist}")
print(f"Time used: {time}")


plt.plot(averageDistOfBest[0], label="100 population")
plt.plot(averageDistOfBest[1], label="250 population")
plt.plot(averageDistOfBest[2], label="500 population")
plt.xlabel('Generations')
plt.ylabel('Average distance of 5 best distance from each generation')
plt.legend()
plt.show()
