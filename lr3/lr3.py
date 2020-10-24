import sys
import os

sys.path.append(os.path.join(sys.path[0], '../packages'))

from NetworkGraph.DataTable import DataTable
from NetworkGraph.NetworkGraph import NetworkGraph

testDatafoo = ['good_test.txt', 
            'parallel_test.txt', 
            'cycle_test.txt', 
            'initial_test.txt', 
            'finishing_test.txt', 
            'bad_test.txt',
            'example.txt']

testData = ['six.txt']

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
