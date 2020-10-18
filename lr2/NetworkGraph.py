# сетевой граф

# internal import
from DataTable import DataTable
from UserDialog import dialog
from Node import Node
from Row import Row

class NetworkGraph(object):
    
    # сетевой граф представляет собой список вершин, связанных ребрами через список указателей
    # а так же связанную с ним выходную таблицу данных

    def __init__(self):
        self.dataTable = None
        self.ngTable = None # network graph table
        self.initialNode = None
        self.nodes = []

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
                parallelActivity = nodeA.findChild(row.B) # посмотреть заранее не существет ли параллельная работа
                nodeA.addChild(nodeB, row.t)

                # выполнить анализ сетевого графа после добавления работы

                # 1) на наличие петель
                if nodeA.val == nodeB.val:
                    print('Обработка строки '+row.toString()+'\nОбнаружена петля. Работа будет удалена.')
                    nodeA.removeChild(row.B, row.t)
                    continue

                # 2) проверить наличие параллельной работы (тогда циклов нет в силу алгоритма)
                if parallelActivity != None:
                    reply = dialog('Обработка строки (#1) ' + row.toString() + '\nОбнаружена параллельная работа (#2): ' + nodeA.childToStr(row.B, parallelActivity['w']) + '\nВы можете:' +
                                   '\nУдалить работу (#1) (1)\nУдалить работу (#2) (2)', ['1', '2'])
                    
                    if reply == '1':
                        nodeA.removeChild(row.B, row.t)
                        continue
                    if reply == '2':
                        nodeA.removeChild(row.B, parallelActivity['w'])
                        continue

                # 3) если не было петель и параллельных работ, то проверить на появление циклов
                checkCycle, way = nodeB.checkCycle(nodeA, [nodeA.val])
                if checkCycle:
                    reply = dialog('Обработка строки ' + row.toString() + '\nОбнаружен цикл: ' + str(way) + '\nВы можете:'+
                                   '\nУдалить работу ' + nodeA.childToStr(row.B, row.t) + ' (1)' +
                                   '\nУдалить работу ' + nodeB.childToStr(way[2]) + ' (2)', ['1', '2'])

                    if reply == '1': # удаляем добавленную работу
                        nodeA.removeChild(row.B, row.t)
                        continue
                    elif reply == '2': # удаляем ранее добавленную работу
                        nodeBChild = nodeB.findChild(way[2])
                        nodeB.removeChild(nodeBChild['ptr'].val, nodeBChild['w'])

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
                            fictiveInitialNode.addChild(self.findNode(node), 0)
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
                            self.findNode(node).addChild(fictiveFinishingNode, 0)
            finishingNodes = self.getAllFinishingNodes()

        # 4) формирование выходной таблицы графа
        self.ngTable = DataTable(self.dataTable.header + ' network graph')
        for node in self.nodes:
            if node.childs != None:
                for child in node.childs:
                    self.ngTable.addRow(node.val, child['ptr'].val, child['w'])


    # удаление узла из графа
    def removeNode(self, val):
        removeable = self.findNode(val)
        # подчистить работы, входящие в это событие
        for node in self.nodes:
            node.removeChild(val)
        self.nodes.remove(removeable) # удалить вершину графа

    def findNode(self, val):
        for node in self.nodes:
            if node.val == val:
                return node
        return None

            
    # получение вершин, в которые нет ни одного вхождения (начальные)
    def getAllInitialNodes(self):
        notInitial = []
        for node in self.nodes:
            if node.childs != None:
                for child in node.childs:
                    notInitial.append(child['ptr'].val)
        notInitial = set(notInitial)
        return list(set(self.getAllNodes()) - notInitial)

    # получение вершин, из которых не выходят ребра (завершающие)
    def getAllFinishingNodes(self):
        return [node.val for node in self.nodes if node.childs == None]

    # получение всех вершин
    def getAllNodes(self):
        return [node.val for node in self.nodes]








