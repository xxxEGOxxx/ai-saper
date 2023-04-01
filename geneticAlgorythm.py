import random


def geneticAligouwu(whereMines):
    populationSize = 120
    topSize = 20
    mutationCount = 5
    genCount = 500

    def distance(xfrom, yto):
        # print(xfrom[0],yto[0],xfrom[1],yto[1])
        return abs(xfrom[0] - yto[0]) + abs(xfrom[1] - yto[1])

    # distance ^

    def fitness(route):
        routescore = 0
        startingPoint = (0, 0)
        routescore += distance(startingPoint, route[0])
        for i in range(0, len(route) - 1):
            if i != (len(route) - 2):
                routescore += distance(route[i], route[i + 1])
        return routescore

    # fitness ^

    def evaluation(population):
        for i in range(0, len(population)):
            # print(str(population[i]) + " nr: " + str(i))
            population[i][-1] = fitness(population[i])

    # evaluation(distance)

    def Davis(p1, p2):
        child = []
        childP1 = []
        childP2 = []

        geneA = int(random.random() * len(p1))
        geneB = int(random.random() * len(p1))

        start = min(geneA, geneB)
        end = max(geneA, geneB)

        for i in range(start, end):
            childP1.append(p1[i])

        childP2 = [item for item in p2 if item not in childP1]

        child = childP1 + childP2
        return child

    # breeding

    def produceNextGeneration(population):
        # print(population[0])
        evaluation(population)
        population.sort(key=lambda eme: eme[-1])
        """tempprintscore = []
            for i in range(0, 10):
                tempprintscore.append(population[i][-1])
            print(tempprintscore)"""
        # print("Best dist: " + str(population[0][-1]))
        # sorting sorted

        newGeneration = []
        for i in range(0, topSize):
            newGeneration.append(population[i])
            # print("elite child: " + str(population[i]) + str(i))
        # elitism
        for i in range(0, len(population) - topSize):
            child = Davis(population[i], population[len(population) - i - 1])
            newGeneration.append(child)
            # print("breed child: " + str(child) + "nr: " + str(i+topSize) + " / " + str(i))
        # fill rest of generation with breeding
        for i in range(mutationCount):
            mO = int(random.random() * len(population))
            # MutatingOrganism
            gene1 = int(abs(random.random() * len(newGeneration[mO]) - 1))
            gene2 = int(abs(random.random() * len(newGeneration[mO]) - 1))
            geneTemp = newGeneration[mO][gene1]
            newGeneration[mO][gene1] = newGeneration[mO][gene2]
            newGeneration[mO][gene2] = geneTemp
        # mutation by swapping mines
        return newGeneration

    def geneticAlgorithm(population, generations):
        currentBestRoute = []
        currentHighScore = 9999999999999
        for i in range(0, generations):
            population = produceNextGeneration(population)
            if population[0][-1] < currentHighScore:
                currentBestRoute = population[0]

        print("Najlepszy dystans: " + str(population[0][-1]) + " / " + str(currentBestRoute[-1]) + " <3")
        return currentBestRoute

    # whereMines = []
    # for encounter in self.current_map.encounters:
    #    whereMines.append((encounter.position_x, encounter.position_y))
    # mines(coordinates) ^
    population = []
    for i in range(0, populationSize):
        tempPopulation = random.sample(whereMines, len(whereMines))
        tempPopulation.append(0)
        population.append(tempPopulation)
    # generation
    ####################################################################################

    route = geneticAlgorithm(population, genCount)
    route.pop()
    # END OF GENETIC ALGORITHM
    ####################################################################################
    return route
