import time, timeit
numbers = None

def read_file(filename):
    nums = []
    with open(filename) as f:
        for line in f.readlines():
            nums.append(int(line))
    return tuple(nums)


def two_sum(t, hash_table):
    global numbers # read only
    for n in numbers:
        hash_table[n] = True
        if hash_table.get(t - n) and (2 * n != t):
            return 1        
    return 0

def two_sum_local_hashtable(t):
    global numbers # read only
    hash_table = {}
    for n in numbers:
        if hash_table.get(t - n) and (2 * n != t):
            return 1
        hash_table[n] = True
    return 0

def count_two_sum_normal(tValues):
    start = timeit.default_timer()
    count = 0
    hash_table = {}
    for t in tValues:
        if two_sum(t, hash_table):
            count += 1
    print count
    stop = timeit.default_timer()
    print "normal two sum time elaplse:", stop - start

def count_two_sum_multi_process(tValues):    
    from multiprocessing import Pool
    start = timeit.default_timer()
    pool = Pool(5)
    results = pool.map(two_sum_local_hashtable, tValues)    
    print sum(results)
    stop = timeit.default_timer()
    print "multiple process time elaplse:", stop - start

def count_two_sum_sorted(numbers, tValues):
    start = timeit.default_timer()
    snumbers = sorted(numbers)
    total = len(snumbers)
    hash_table = {}
    count = 0    
    for t in tValues:
        for n in snumbers:
            if n > t/2 and len(hash_table) == total:
                break
            hash_table[n] = True
            if hash_table.get(t - n) and (2 * n != t):
                count += 1
                break            
    print count
    stop = timeit.default_timer()
    print "sorted two sum time elaplse:", stop - start



if __name__ == '__main__':
    
    tValues = range(-10000,10000 + 1) 
    numbers = read_file('2sum.txt')
    # numbers = [10000,-10000,5464564,134,1344,899,0,1] # for test, result must be 17
    count_two_sum_sorted(numbers, tValues)
    count_two_sum_normal(tValues)
    count_two_sum_multi_process(tValues)


    

