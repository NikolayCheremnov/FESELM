# узел графа

class Node(object):
    
    def __init__(self, val):
        self.childs = None
        self.val = val

    # добавление потомка
    def addChild(self, child, weight):
        if self.childs == None:
            self.childs = [{'ptr': child, 'w': weight}]
        else:
            self.childs.append({'ptr': child, 'w': weight})

    # удаление потомка
    def removeChild(self, childVal, weight=None):
        if self.childs != None:
            removable = None
            for child in self.childs:
                if child['ptr'].val == childVal and (weight == None or child['w'] == weight):
                    removable = child
                    break
            if removable != None:
                self.childs.remove(removable)
                if len(self.childs) == 0:
                    self.childs = None

    # проверка на наличие циклов из вершины node
    def checkCycle(self, node, way):
        if self == node:
            return True, way + [self.val]
        elif self.childs != None:
            for child in self.childs:
                res, way = child['ptr'].checkCycle(node, way + [self.val])
                if res == True:
                    return res, way
        return False, way[:-1]

    # получение строки работы между вершиной и потомком
    def childToStr(self, childVal, weight=None):
        child = self.findChild(childVal, weight)
        if child != None:
            return 'A: ' + str(self.val) + ' B: ' + str(child['ptr'].val) + ' t: ' + str(child['w'])
        return None

    # поиск потомка по значению
    def findChild(self, childVal,weight=None):
        if self.childs == None:
            return None
        for child in self.childs:
            if child['ptr'].val == childVal and (weight == None or child['w'] == weight):
                return child
        return None

    # вывод всех путей из начальной вершины до конечной
    def displayAllWays(self, buf):
        buf.append(self.val)
        if self.childs == None:
            print(buf)
        else:
            for child in self.childs:
                buf = child['ptr'].displayAllWays(buf)
        return buf[:-1]



