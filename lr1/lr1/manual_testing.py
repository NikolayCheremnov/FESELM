import lr1
import sys

matrix_data = [
        # first test
        [[20, 30, 15],
        [75, 20, 35],
        [25, 80, 25],
        [85, 5, 45]],

        # second test
        [[19, 30, 41, 49],
         [51, 38, 10, 20],
         [73, 18, 81, 11]],

        # third test
        [[9, 15, 7],
         [3, 11, 5],
         [8, 6, 12],
         [10, 7, 4]]
    ]

q_data = [
            # first test
            [0.3, 0.2, 0.5],

            # second test
            [0.6, 0.1, 0.1, 0.2],

            # third test
            [0.33, 0.5, 0.17]
        ]

mode = 2

if mode == 2:
    filename = open('dump.txt', 'w')
    sys.stdout = filename

for payMatrix, Q in zip(matrix_data, q_data):
    print('\n\n=====\n|!|\n=====')
    lr1.PrintExample((payMatrix, Q))
    riskMatrix = lr1.getRiskMatrix(payMatrix)
    lr1.PrintExample(None, riskMatrix)
    print('Критерий Вальда:', lr1.Wald(payMatrix))
    print('Критерий Сэвиджа:', lr1.Savage(riskMatrix))
    print('Критерий Гурвица, E = 1.0', lr1.Hurwitz(payMatrix, 1.0))
    print('Вероятностный критерий:', lr1.PC((payMatrix, Q)))

if mode == 2:
    filename.close()
    sys.stdout = sys.__stdout__