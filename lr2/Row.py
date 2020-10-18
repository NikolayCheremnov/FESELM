# строка таблицы исходных данных

class Row(object):
    
    def __init__(self, A, B, t):
        self.A = A
        self.B = B
        self.t = t
        self.flag = False

    def toString(self):
        return 'A: ' + str(self.A) + ' B: ' + str(self.B) + ' t: ' + str(self.t)


