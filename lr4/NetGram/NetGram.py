import sys
import os

sys.path.append(os.path.join(sys.path[0], '../../packages')) # add packages path

from NetworkGraph.DataTable import DataTable
from NetworkGraph.NetworkGraph import NetworkGraph

from tkinter import *

if __name__ == "__main__": 
    print('Введите имя файла с исходными данными: ', end='')
    fname = input()                         # input data file 
    dt = DataTable(fname[:-4], fname)       # read data table
    print('Исходная таблица:')
    dt.print()                              # исходная таблица

    # далее работа с сетевым графом
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
    
    # подготовим холст для рисования
    root = Tk()
    root.title("Gantt diagram")
    canvas = Canvas(root, width=1920, height=1080, bg='white')
    
    # разлиновать холст
    for i in range(0, 1930, 10):
        canvas.create_line(i, 0, i, 1080, fill='light gray')
    for i in range(0, 1090, 10):
        canvas.create_line(0, i, 1920, i, fill='light gray')

    # добавить надписи работ и отобразить их выполнение по раннему сроку выполнения соответствующей работы
    workLbl = Label(canvas, text='Работы:')
    workLbl.place(x=0, y=0)
    yPos = 20 
    dx = 50
    for work in ng.edges:
        workLabel = Label(canvas, text=str(work.parentPtr.value)+':'+str(work.childPtr.value), font=("Comic Sans MS", 7, "bold"))
        workLabel.place(x=20, y=yPos)
        canvas.create_rectangle(dx+work.parentPtr.early*10, yPos, dx+(work.parentPtr.early+work.value)*10, yPos+10, fill='blue') # по ранним срокам
        canvas.create_rectangle(dx+work.parentPtr.late*10, yPos+10, dx+(work.parentPtr.late+work.value)*10, yPos+20, fill='red') # по ранним срокам
        yPos += 20
    
    # написать мануал
    nullLbl = Label(canvas, text='0')
    nullLbl.place(x=dx-5, y=yPos)
    yPos += 20
    lbl1 = Label(canvas, text='по ранним срокам:')
    lbl1.place(x=20, y = yPos)
    canvas.create_rectangle(200, yPos, 210, yPos+10, fill='blue')
    lbl2 = Label(canvas, text='по поздним срокам:')
    lbl2.place(x=20, y=yPos+20)
    canvas.create_rectangle(200, yPos+20, 210, yPos+10+20, fill='red')
    lbl3 = Label(canvas, text='одна клетка = одна единица времени')
    lbl3.place(x=20, y=yPos+40)

    canvas.pack()
    root.mainloop()     # запуск формы
    # далее код после закрытия холста
    print('after all')


   