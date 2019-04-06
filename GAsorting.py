import random

def calFitness(array):
    size = len(array)

    count = 0
    for i in range(size - 1):
        if array[i + 1] > array[i]:
            count += 1

    fitneess = count / (size - 1)
    return fitneess

# swap random two item in the list
def randomSwap(array):
    index1 = random.randint(0, len(array) - 1)
    index2 = random.randint(0, len(array) - 1)

    while(index1 == index2):
        index2 = random.randint(0, len(array) - 1)

    tmp = array[index1]
    array[index1] = array[index2]
    array[index2] = tmp

    return array

class chromosome:
    array = []
    fitneess = 0

    def __init__(self, _array):
        self.array = _array
        self.fitneess = calFitness(_array)

def crossOver(chromosome1, chromosome2):
    parent1 = chromosome1.array
    parent2 = chromosome2.array
    child = [None] * len(parent1)

    index1 = random.randint(0, len(parent1) - 1)
    index2 = random.randint(0, len(parent1) - 1)

    while (index1 == index2):
        index2 = random.randint(0, len(parent1) - 1)

    tmp = index1
    index1 = min(index1, index2)
    index2 = max(tmp, index2)

    # print(index1, index2)
    # copy one part of the array directly
    for i in range(index1, index2 + 1):
        child[i] = parent1[i]

    # fill in the missing part from parent2
    count = 0
    if count == index1:
        count = index2 + 1

    for i in range(len(parent2)):
        if parent2[i] not in child:
            child[count] = parent2[i]
            count += 1
            if count == index1:
                count = index2 + 1

    return child

def GAsorting(arr):
    geneticPool = []

    # generate two parents
    geneticPool.append(chromosome(arr))
    geneticPool.append(chromosome(randomSwap(geneticPool[0].array.copy())))

    isDone = False
    iterateTimes = 0
    # loop here
    while(not isDone):
        fitnessSum = 0
        for i in geneticPool:
            fitnessSum += i.fitneess

        # 1. selection
        isSelected = False
        parent1Idx = -1
        parent2Idx = -1

        while(not isSelected):
            parent1Fit = random.random() * fitnessSum
            parent2Fit = random.random() * fitnessSum
            #print(parent1Fit, parent2Fit)

            parent1Idx = -1
            parent2Idx = -1
            tmpFitnessSum = 0
            for i in range(len(geneticPool)):
                tmpFitnessSum += geneticPool[i].fitneess
                if(parent1Fit <= tmpFitnessSum and parent1Idx == -1):
                    parent1Idx = i
                if(parent2Fit <= tmpFitnessSum and parent2Idx == -1):
                    parent2Idx = i

            if (parent1Idx != parent2Idx):
                isSelected = True

        # 2. crossOver
        child = crossOver(geneticPool[0], geneticPool[1])
        geneticPool.append(chromosome(child))

        # 3. mutate
        mutatepro = random.random()
        if(mutatepro < 0.3):
            mutateIdx = random.randint(0, len(geneticPool) - 1)
            mutateArr = geneticPool[mutateIdx].array.copy()
            randomSwap(mutateArr)
            geneticPool.append(chromosome(mutateArr))

        # 4. check whether sorted and size of genetic pool
        maxFitness = -1.0
        maxIdx = -1
        minFitness = +2.0
        minIdx = -1

        for i in range(len(geneticPool)):
            if geneticPool[i].fitneess > maxFitness:
                maxFitness = geneticPool[i].fitneess
                maxIdx = i
            if geneticPool[i].fitneess < minFitness:
                minFitness = geneticPool[i].fitneess
                minIdx = i

        if maxFitness == 1:
            print("Total take ", iterateTimes, " times: ", geneticPool[maxIdx].array)
            isDone = True
        else:
            print("#", iterateTimes, ": ", geneticPool[maxIdx].array)
            while(len(geneticPool) > 20):
                geneticPool.pop(minIdx)
                minFitness = +2.0
                for i in range(len(geneticPool)):
                    if geneticPool[i].fitneess < minFitness:
                        minFitness = geneticPool[i].fitneess
                        minIdx = i

        iterateTimes += 1

a = [6, 4, 5, 8, 2, 0, 3, 1, 7, 9]
GAsorting(a)