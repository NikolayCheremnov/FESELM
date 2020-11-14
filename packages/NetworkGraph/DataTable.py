# таблица исходных данных

from NetworkGraph.Row import Row
import prettytable 

class DataTable(object):
    
    def __init__(self, header = 'undefined_header', fname = None):

        self.header = header
        self.rows = []
        if fname != None:      
            with open(fname, 'r') as f:
                data = f.read().splitlines()
                self.header = data[0]
                data = data[1:]
                for row in data:
                    tokens = row.split()
                    self.rows.append(Row(int(tokens[0]), int(tokens[1]), int(tokens[2])))
    
    # получения множества событий 
    def getAllEvents(self):
        return list(set(self.getAllEventsA() + self.getAllEventsB()))
        

    # получение множества событий, из которых исходят работы
    def getAllEventsA(self):
        events = []
        for row in self.rows:
            if not (row.A in events):
                events.append(row.A)
        return events

    # получение множества событий, в которые входят работы
    def getAllEventsB(self):
        events = []
        for row in self.rows:
            if not (row.B in events):
                events.append(row.B)
        return events

    # удаление строки по позиции
    def removeRow(self, A, B, t):
        removeable = None
        for row in self.rows:
            if row.A == A and row.B == B and row.t == t:
                removeable = row
        if removeable == None:
            return None
        else:
            self.rows.remove(removeable)
            return removeable

    # добавление строки в конец таблицы
    def addRow(self, A, B, t):
        self.rows.append(Row(A, B, t))

    # добавление строки в начало таблицы
    def addRowToTop(self, A, B, t):
        self.rows = [Row(A, B, t)] + self.rows

    # вывод таблицы на экран
    def print(self):
        print(self.header)
        th = ['A', 'B', 't']
        table = prettytable.PrettyTable(th)

        for row in self.rows:
            table.add_row([row.A, row.B, row.t])
    
        print(table)

    # процедура освобождения значения -1 под фиктивные вершины
    def releaseFictiveValue(self):
        for row in self.rows:
            if row.A < 0:
                row.A -= 2
            if row.B < 0:
                row.B -= 2


