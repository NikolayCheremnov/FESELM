# сетевой граф

# external imports
import prettytable

# internal import
from NetworkGraph.DataTable import DataTable
from UserDialog.UserDialog import dialog
from NetworkGraph.Node import Node
from NetworkGraph.Row import Row
from NetworkGraph.Edge import Edge

class NetworkGraph(object):
    
    # сетевой граф представляет собой список вершин, связанных ребрами через список указателей
    # а так же связанную с ним выходную таблицу данных

    def __init__(self):
        self.dataTable = None
        self.ngTable = None # network graph table
        self.initialNode = None
        self.finishingNode = None
        self.nodes = []
        self.edges = []

    # вывод таблицы параметров работ
    def printEdgeParameters(self):
        th = ['Работа', 'Длительность', 'Полный резерв', 'Независимый резерв']
        table = prettytable.PrettyTable(th)
        for edge in self.edges:
            table.add_row([str(edge.parentPtr.value)+':'+str(edge.childPtr.value), edge.value, edge.fullReserve, edge.independentReserve])
        print(table)

    # инициализация параметров работ
    def initializingEdgeParameters(self):
        for edge in self.edges:
            edge.initializeReserves()

    # вывод таблицы параметров событий
    def printNodeParameters(self):
        th = ['Событие', 'Ранний срок', 'Поздний срок', 'Резерв']
        table = prettytable.PrettyTable(th)
        for node in self.nodes:
            table.add_row([node.value, node.early, node.late, node.reserve])
        print(table)

    # построение сетевого графика
    def ngCreating(self, dataTable):

        self.dataTable = dataTable

        # 1. инициализация событий в сетевом графе
        events = self.dataTable.getAllEvents()

        for event in events:
            self.nodes.append(Node(event))

        # 2. обработка строк таблицы исходных данных
        for row in self.dataTable.rows:
               
                # добавить очередную работу
                nodeA = self.findNode(row.A)
                nodeB = self.findNode(row.B)
                parallelActivity = nodeA.findEdge(row.B) # посмотреть заранее не существет ли параллельная работа
                self.addEdge(nodeA, nodeB, row.t)

                # выполнить анализ сетевого графа после добавления работы

                # 1) на наличие петель
                if nodeA.value == nodeB.value:
                    print('Обработка строки '+row.toString()+'\nОбнаружена петля. Работа будет удалена.')
                    self.removeEdge(nodeA, nodeB, row.t)
                    continue

                # 2) проверить наличие параллельной работы (тогда циклов нет в силу алгоритма)
                if parallelActivity != None:
                    reply = dialog('Обработка строки (#1) ' + row.toString() + '\nОбнаружена параллельная работа (#2): ' + nodeA.edgeToStr(row.B, parallelActivity.value) + '\nВы можете:' +
                                   '\nУдалить работу (#1) (1)\nУдалить работу (#2) (2)', ['1', '2'])                 
                    if reply == '1':
                        self.removeEdge(nodeA, nodeB, row.t)
                        continue
                    if reply == '2':
                        self.removeEdge(nodeA, nodeB, parallelActivity.value)
                        continue

                # 3) если не было петель и параллельных работ, то проверить на появление циклов
                checkCycle, way = nodeB.checkCycle(nodeA, [nodeA.value])
                while checkCycle:
                    reply = dialog('Обработка строки ' + row.toString() + '\nОбнаружен цикл: ' + str(way) + '\nВы можете:'+
                                   '\nУдалить работу ' + nodeA.edgeToStr(row.B, row.t) + ' (1)' +
                                   '\nУдалить работу ' + nodeB.edgeToStr(way[2]) + ' (2)', ['1', '2'])
                    if reply == '1': # удаляем добавленную работу
                        self.removeEdge(nodeA, nodeB, row.t)
                        continue
                    elif reply == '2': # удаляем ранее добавленную работу
                        nodeBEdge = nodeB.findEdge(way[2])
                        self.removeEdge(nodeB, nodeBEdge.childPtr, nodeBEdge.value)
                    checkCycle, way = nodeB.checkCycle(nodeA, [nodeA.value])

        # 3. определить начальное и завершающее соыбтие в сетевом графе
        
        # 3.1) определение начальных состояний
        initialNodes = self.getAllInitialNodes()
        fictiveInitialNode = None
        while len(initialNodes) != 1:
            if fictiveInitialNode == None: # пока фиктивная еще не введена
                reply = dialog('В сетевом графе нет единственного начального события.\nВы можете:' + 
                      '\nВыбрать одно начальное событие (1)' +
                      '\nВвести фиктивное начальное событие и удалить ненужные события (2)', ['1', '2'])
                if reply == '1':
                    reply = int(dialog('Введите событие, которое оставить (доступны ' + str(initialNodes) + ')', [str(val) for val in initialNodes]))
                    for removeable in initialNodes:
                        if removeable != reply:
                            self.removeNode(removeable)
                elif reply == '2':
                    fictiveInitialNode = Node(-1)
                    self.nodes.append(fictiveInitialNode)
            else: # если есть фиктивная, то определить какие события оставить, а какие удалить
                for node in initialNodes:
                    if node != -1:
                        reply = dialog('Событие ' + str(node) + ' удалить (1) или оставить (2) ', ['1', '2'])
                        if reply == '1': # событие удаляется
                            self.removeNode(node)
                        elif reply == '2': # событие сохраняется
                            self.addEdge(fictiveInitialNode, self.findNode(node), 0)
            initialNodes = self.getAllInitialNodes()
        self.initialNode = self.findNode(initialNodes[0])

        # 3.2) определение заверщающего состояния
        finishingNodes = self.getAllFinishingNodes()
        fictiveFinishingNode = None
        while len(finishingNodes) != 1:
            if fictiveFinishingNode == None: # пока фиктивная еще не введена
                reply = dialog('В сетевом графе нет единственного конечного события.\nВы можете:' + 
                      '\nВыбрать одно конечное событие (1)' +
                      '\nВвести фиктивное конечное событие и удалить ненужные события (2)', ['1', '2'])
                if reply == '1':
                    reply = int(dialog('Введите событие, которое оставить (доступны ' + str(finishingNodes) + ')', [str(val) for val in finishingNodes]))
                    for removeable in finishingNodes:
                        if removeable != reply:
                            self.removeNode(removeable)
                elif reply == '2':
                    fictiveFinishingNode = Node(-2)
                    self.nodes.append(fictiveFinishingNode)
            else: # если есть фиктивная, то определить какие события оставить, а какие удалить
                for node in finishingNodes:
                    if node != -2:
                        reply = dialog('Событие ' + str(node) + ' удалить (1) или оставить (2) ', ['1', '2'])
                        if reply == '1': # событие удаляется
                            self.removeNode(node)
                        elif reply == '2': # событие сохраняется
                            self.addEdge(self.findNode(node), fictiveFinishingNode, 0)
            finishingNodes = self.getAllFinishingNodes()
        self.finishingNode = self.findNode(finishingNodes[0])

        # 4) формирование выходной таблицы графа
        self.ngTable = DataTable(self.dataTable.header + ' network graph')
        for node in self.nodes:
            if node.outEdges != None:
                for edge in node.outEdges:
                    self.ngTable.addRow(node.value, edge.childPtr.value, edge.value)

    # добавление ребра в граф
    def addEdge(self, parentPtr, childPtr, value):
        edge = Edge(parentPtr, childPtr, value)
        self.edges.append(edge)
        if parentPtr.outEdges == None:
            parentPtr.outEdges = [edge]
        else:
            parentPtr.outEdges.append(edge)
        if childPtr.inEdges == None:
            childPtr.inEdges = [edge]
        else:
            childPtr.inEdges.append(edge)

    # удаление ребра из графа
    def removeEdge(self, parentPtr, childPtr, value=None):
        if parentPtr.outEdges != None:
            removable = None
            for edge in parentPtr.outEdges:
                if (value == None or edge.value == value) and edge.childPtr == childPtr:
                    removable = edge
                    break
            if removable != None:
                parentPtr.outEdges.remove(removable)
                if len(parentPtr.outEdges) == 0:
                    parentPtr.outEdges = None
                childPtr.inEdges.remove(removable)
                if len(childPtr.inEdges) == 0:
                    childPtr.inEdges = None
                self.edges.remove(removable)

    # удаление узла из графа (по значению)
    def removeNode(self, val):
        removeable = self.findNode(val)
        # подчистить работы, входящие в это событие
        inEdge = None
        outEdge = None
        for edge in self.edges:
            if edge.parentPtr == removeable:
                outEdge = edge
            elif edge.childPtr == removeable:
                inEdge = edge
        if inEdge != None:
            inEdge.parentPtr.outEdges.remove(inEdge)
            self.edges.remove(inEdge)
        if outEdge != None:
            outEdge.childPtr.inEdges.remove(outEdge)
            self.edges.remove(outEdge)
        self.nodes.remove(removeable) # удалить вершину графа

    def findNode(self, value):
        for node in self.nodes:
            if node.value == value:
                return node
        return None

            
    # получение вершин, в которые нет ни одного вхождения (начальные) (значения)
    def getAllInitialNodes(self):
        notInitial = []
        for node in self.nodes:
            if node.outEdges != None:
                for edge in node.outEdges:
                    notInitial.append(edge.childPtr.value)
        notInitial = set(notInitial)
        return list(set(self.getAllNodes()) - notInitial)

    # получение вершин, из которых не выходят ребра (завершающие) (значения)
    def getAllFinishingNodes(self):
        return [node.value for node in self.nodes if node.outEdges == None]

    # получение всех вершин (значения)
    def getAllNodes(self):
        return [node.value for node in self.nodes]










