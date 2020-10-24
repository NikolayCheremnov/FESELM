# узел графа

from NetworkGraph.Edge import Edge

class Node(object):
    
    def __init__(self, value):
        self.outEdges = None # исходящие ребра (строятся при построении)
        self.inEdges = None  # входящие ребра
        self.value = value
        # parameters
        self.early = None
        self.late = None
        self.reserve = None

    # определение параметра "ранний срок"
    def initializingEarly(self, isInitial=False):
        self.early = (lambda: 0 if isInitial else max([inEdge.parentPtr.early + inEdge.value for inEdge in self.inEdges if inEdge.parentPtr.early != None]))() 
        if self.outEdges != None:
            for outEdge in self.outEdges:
                outEdge.childPtr.initializingEarly()

    # определение парметра "поздний срок"
    def initializingLate(self, isInitial=False):
        self.late = (lambda: self.early if isInitial else min([outEdge.childPtr.late - outEdge.value for outEdge in self.outEdges if outEdge.childPtr.late != None]))()
        self.reserve = self.late - self.early
        if self.inEdges != None:
            for inEdge in self.inEdges:
                inEdge.parentPtr.initializingLate()

    # проверка на наличие циклов из вершины node
    def checkCycle(self, node, way):
        if self == node:
            return True, way + [self.value]
        elif self.outEdges != None:
            for edge in self.outEdges:
                res, way = edge.childPtr.checkCycle(node, way + [self.value])
                if res == True:
                    return res, way
        return False, way[:-1]

    # получение строки работы между вершиной и потомком
    def edgeToStr(self, childVal, weight=None):
        edge = self.findEdge(childVal, weight)
        if edge != None:
            return 'A: ' + str(self.value) + ' B: ' + str(edge.childPtr.value) + ' t: ' + str(edge.value)
        return None

    # поиск потомка по значению
    def findEdge(self, childVal, weight=None):
        if self.outEdges == None:
            return None
        for edge in self.outEdges:
            if edge.childPtr.value == childVal and (weight == None or edge.value == weight):
                return edge
        return None
    
    # вывод всех критических путей
    def displayAllCriticalWays(self, buf):
        buf.append(self.value)
        if self.outEdges == None:
            print(buf)
        else:
            for edge in self.outEdges:
                if edge.fullReserve == 0:
                    buf = edge.childPtr.displayAllCriticalWays(buf)
        return buf[:-1]

    # вывод всех путей из начальной вершины до конечной
    def displayAllWays(self, buf):
        buf.append(self.value)
        if self.outEdges == None:
            print(buf)
        else:
            for edge in self.outEdges:
                buf = edge.childPtr.displayAllWays(buf)
        return buf[:-1]



