from DataTable import DataTable
from NetworkGraph import NetworkGraph

testData = ['good_test.txt', 
            'parallel_test.txt', 
            'cycle_test.txt', 
            'initial_test.txt', 
            'finishing_test.txt', 
            'bad_test.txt',
            'example.txt']

if __name__ == "__main__":
    for test in testData:
        dt = DataTable(test[:-4], test)
        dt.print()
        ng = NetworkGraph()
        ng.ngCreating(dt)
        ng.ngTable.print()
        print('Пути в сетевом графе:')
        ng.initialNode.displayAllWays([])


