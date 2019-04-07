import random
import numpy as np
import matplotlib.pyplot as plt

def calFitness(array):
    size = len(array)
    allCount = 0

    count = 0
    for i in range(size):
        for j in range(i + 1, size):
            if array[j] > array[i]:
                count += 1
            allCount += 1

    fitneess = count / allCount
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
    fitnessTrend = []
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
            print("GA Total take ", iterateTimes, " times: ", geneticPool[maxIdx].array)
            isDone = True
        else:
            #print("#", iterateTimes, ": ", geneticPool[maxIdx].array)
            while(len(geneticPool) > 10):
                geneticPool.pop(minIdx)
                minFitness = +2.0
                for i in range(len(geneticPool)):
                    if geneticPool[i].fitneess < minFitness:
                        minFitness = geneticPool[i].fitneess
                        minIdx = i

        iterateTimes += 1
        fitnessTrend.append(maxFitness)

    return fitnessTrend

# bubble
def bubbleSort(arr):
    fitnessArr = []
    n = len(arr)
    count = 0

    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

            tmpFitness = calFitness(arr)
            fitnessArr.append(tmpFitness)
            count += 1

    print("Bubble Total take ", count, " times: ", arr)
    return fitnessArr

arr = np.arange(30)
np.random.shuffle(arr)
a = list(arr)

b = a.copy()
GAfit = GAsorting(b)

b = a.copy()
bubblefit = bubbleSort(b)

plt.plot(GAfit)
plt.plot(bubblefit)
plt.show()

# sumIterateTimes = 0
# for i in range(100):
#     sumIterateTimes += GAsorting(a)
#
# print("Average Times: ", sumIterateTimes / 100)