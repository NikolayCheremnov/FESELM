import random
import prettytable 
import copy

# test generator
def CreateTest(m = 4, n = 4, min = 1, max = 10, PFlag = False):
    payMatrix = []
    for i in range(m):
        payMatrix.append([])
        for j in range(n):
            payMatrix[i].append(random.randint(min, max))
    if PFlag:
        PRest = 1
        Q = []
        for j in range(n - 1):
            pseudo = random.uniform(0, PRest)
            Q.append(round(pseudo, 5))
            PRest -= pseudo

        Q.append(round(PRest, 5))

        return payMatrix, Q
    
    return payMatrix, None
    
# print example
def PrintExample(genRes, riskMatrix = None):
    payMatrix = []
    Q = None
    if riskMatrix == None:
        print('Платежная матрица:')
        payMatrix = genRes[0]
        Q = genRes[1]
    else:
        print('Матрица рисков:')
        payMatrix = riskMatrix
    columnsNumb = len(payMatrix[0])
    rowsNumb = len(payMatrix)
    th = ['А\П']
    if Q == None:
        th = th + [i for i in range(columnsNumb)]
    else:
        th = th + [str(i) + ', Q=' + str(Q[i]) for i in range(columnsNumb)]   

    payMatrixTable = prettytable.PrettyTable(th)

    for i in range(rowsNumb):
        payMatrixTable.add_row([i] + payMatrix[i])

    print(payMatrixTable)
    
# probabilistic criterion <=> PC
def PC(genRes):
    payMatrix = genRes[0]
    Q = genRes[1]
    if Q == None:
        raise Exception('No probabilities')

    riskMatrix = getRiskMatrix(payMatrix)
    averageRisk = [sum([q * r for q, r in zip(Q, riskMatrix[i])]) for i in range(len(riskMatrix))]

    strategies = [i for i in range(len(payMatrix)) if averageRisk[i] == min(averageRisk)]
    return min(averageRisk), strategies

# get risk matrix
def getRiskMatrix(payMatrix):
    riskMatrix = copy.deepcopy(payMatrix)

    for j in range(len(payMatrix[0])):
        max = payMatrix[0][j]
        for i in range(len(payMatrix)):
            if payMatrix[i][j] > max:
                max = payMatrix[i][j]
        
        for i in range(len(payMatrix)):
            riskMatrix[i][j] = max - riskMatrix[i][j]
    
    return riskMatrix

# Wald's criterion
def Wald(payMatrix):
    minima = [min(payMatrix[i]) for i in range(len(payMatrix))]
    strategies = [i for i in range(len(minima)) if minima[i] == max(minima)]
    return max(minima), strategies

# Savage criterion
def Savage(riskMatrix):
    maxima = [max(riskMatrix[i]) for i in range(len(riskMatrix))]
    strategies = [i for i in range(len(maxima)) if maxima[i] == min(maxima)]
    return min(maxima), strategies

# Hurwitz criterion
def Hurwitz(payMatrix, E = 0.5):
    criteria = [round(E*min(payMatrix[i]) + (1 - E)*max(payMatrix[i])) for i in range(len(payMatrix))]
    strategies = [i for i in range(len(criteria)) if criteria[i] == max(criteria)]
    return max(criteria), strategies