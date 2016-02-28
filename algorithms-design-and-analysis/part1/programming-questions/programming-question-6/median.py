from heap import Heap
from tree import SearchTree
import time, timeit


def read_file(filename):
    numbers = []
    with open(filename) as f:
        for line in f.readlines():
            numbers.append(int(line.strip()))
    return numbers


def head_sol(numbers):
    minHeap = Heap()
    maxHeap = Heap(is_max=True)
    median_sum = 0
    k = 0
    for n in numbers:
        k += 1
        m = maxHeap.extract_top()       
        if m != None:
            median_sum += m
            if n > m:
                minHeap.insert(n)
            else:
                maxHeap.insert(n)
        else:
            maxHeap.insert(n)    

        while maxHeap.size() > minHeap.size() + 1:
            m = maxHeap.pop_top()
            minHeap.insert(m)

        while maxHeap.size() < minHeap.size():
            m = minHeap.pop_top()
            maxHeap.insert(m)      

    median_sum += maxHeap.extract_top()
    return median_sum % k


def st_sol(numbers):
    my_tree = SearchTree()
    median_sum = 0
    medians = []
    k = 0
    for n in numbers:
        k += 1
        my_tree.insert(n)
        median_sum += my_tree.root()
    return median_sum % k


if __name__ == '__main__':
    numbers = read_file('median.txt')
    start = timeit.default_timer()
    print head_sol(numbers)
    stop = timeit.default_timer()
    print "heap solution time elaplse:", stop - start

    start = timeit.default_timer()
    print st_sol(numbers)
    stop = timeit.default_timer()
    print "st solution time elaplse:", stop - start
