import sys
import os

sys.path.append(os.path.join(sys.path[0], '../packages'))

from NetworkGraph.DataTable import DataTable
from NetworkGraph.NetworkGraph import NetworkGraph

testData = ['good_test.txt', 
            'six.txt', 
            'test.txt',]

if __name__ == "__main__":
    for test in testData:
        dt = DataTable(test[:-4], test)
        #dt.print()
        ng = NetworkGraph()
        ng.ngCreating(dt)
        ng.ngTable.print()
        ng.initialNode.initializingEarly(True)
        ng.finishingNode.initializingLate(True)
        ng.printNodeParameters()
        ng.initializingEdgeParameters()
        ng.printEdgeParameters()
        print('Критические пути в сетевом графе:')
        ng.initialNode.displayAllCriticalWays([])
        print('Длина критического пути:', ng.finishingNode.early)
