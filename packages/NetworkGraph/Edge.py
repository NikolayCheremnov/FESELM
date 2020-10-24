# ребро графа

class Edge(object):
    
    def __init__(self, parentPtr, childPtr, value):
        self.parentPtr = parentPtr
        self.childPtr = childPtr
        self.value = value
        # параметры
        self.fullReserve = None
        self.independentReserve = None

    def initializeReserves(self):
        self.fullReserve = self.childPtr.late - self.parentPtr.early - self.value
        if self.fullReserve < 0:
            self.fullReserve = None
        self.independentReserve = self.childPtr.early - self.parentPtr.late - self.value
        if self.independentReserve < 0:
            self.independentReserve = None



