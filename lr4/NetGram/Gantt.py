from tkinter import *

def Gantt(ng):
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
    for i in range(0, 100, 5):
        lbl = Label(canvas, text=str(i))
        lbl.place(x=i*10+dx, y=yPos+10)
    yPos += 40
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
