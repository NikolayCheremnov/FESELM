import sys
import os

sys.path.append(os.path.join(sys.path[0], '../../packages')) # add packages path

from NetworkGraph.DataTable import DataTable
from NetworkGraph.NetworkGraph import NetworkGraph
from Gantt import Gantt
from UserDialog.UserDialog import cmdDialog
from UserDialog.UserDialog import message

from tkinter import *

# цикл формирования графа
def ngCycle(dt):
     # работа с сетевым графом
    dt.releaseFictiveValue()
    ng = NetworkGraph()                     # создать граф
    ng.ngCreating(dt)                       # упорядочить в него исходную таблицу
    ng.initialNode.initializingEarly(True)  # посчитпть параметры
    ng.finishingNode.initializingLate(True)
    ng.initializingEdgeParameters()
    print('Таблица упорядоченного сетевого графика: ')
    ng.ngTable.print()                      # напечатать таблицу
    print('Параметры сетевого графика: ')
    ng.printNodeParameters()                # вывести параметры графа
    ng.printEdgeParameters()
    print('Длина критического пути:', ng.finishingNode.early)

    # далее вывести диаграмму ганта для данной итерации
    Gantt(ng)

    return ng

if __name__ == "__main__": 
    print('Введите имя файла с исходными данными: ', end='')
    fname = input()                         # input data file 
    dt = DataTable(fname[:-4], fname)       # read data table
    print('Исходная таблица:')
    dt.print()                              # исходная таблица

    ng = ngCycle(dt)                        # поработать с графом

    # далее код после закрытия холста
    cmd = ['unknown']
    while cmd[0] != 'exit':
        cmd = cmdDialog('Введите команду (help - помощь, exit - завершение работы с графиком)')
        
        # выбрать нужно действие
        if cmd[0] == 'exit':
            exit(0)
        elif cmd[0] == 'help':
            print('Список доступных команд:')
            print('exit - завершить работу')
            print('help - вывести список доступных команд')
            print('add A B t - добавить работу от события A к событию B длительностью t (A, B, t целые >= 0)')
            print('remove A B t - удалить работу от события A к событию B длительностью t (A, B, t целые >= 0)')
        # добавление работы
        elif cmd[0] == 'add':           
            if len(cmd) == 4 and int(cmd[1]) >= 0 and int(cmd[2]) >= 0 and int(cmd[3]) >= 0:
                dt = ng.ngTable
                dt.addRow(int(cmd[1]), int(cmd[2]), int(cmd[3]))
                ng = ngCycle(dt)
            else:
                message('Недопустимые аргументы команды. Изспользуйте help чтобы получить больше информации о командах')
        # удаление работы
        elif cmd[0] == 'remove':
            if len(cmd) == 4 and int(cmd[1]) >= 0 and int(cmd[2]) >= 0 and int(cmd[3]) >= 0:
                dt = ng.ngTable
                removeable = dt.removeRow(int(cmd[1]), int(cmd[2]), int(cmd[3]))
                if removeable == None:
                    message('Данной работы не существует')
                else:
                    ng = ngCycle(dt)
            else:
                message('Недопустимые аргументы команды. Изспользуйте help чтобы получить больше информации о командах')

