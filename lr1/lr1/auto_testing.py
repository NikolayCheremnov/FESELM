import lr1
import random
import sys

N = 3
mode = 2

if mode == 2:
    filename = open('dump.txt', 'w')
    sys.stdout = filename


for i in range(N):
    print('\n\n=====\n|', i, '|\n=====')
    genRes = lr1.CreateTest(random.randint(3, 6), random.randint(3, 6), 5, 25, True)
    payMatrix = genRes[0]
    Q = genRes[1]
    lr1.PrintExample(genRes)
    riskMatrix = lr1.getRiskMatrix(payMatrix)
    lr1.PrintExample(None, riskMatrix)
    print('Критерий Вальда:', lr1.Wald(payMatrix))
    print('Критерий Сэвиджа:', lr1.Savage(riskMatrix))
    print('Критерий Гурвица, E = 0.6', lr1.Hurwitz(payMatrix, 0.6))
    print('Вероятностный критерий:', lr1.PC((payMatrix, Q)))

if mode == 2:
    filename.close()
    sys.stdout = sys.__stdout__
