

def loadIntegers(filename):
    with open(filename) as f:
        content = f.readlines()
    if not content:
        return None
    array = []
    for c in content:
        array.append(int(c))
    return array

def count_each_comparision(array_len):
	return array_len - 1

def fetch_1st_as_pivot(array, left, right):
	return array[left]

def fetch_final_as_pivot(array, left, right):
	swap(array, left, right)
	return array[left]

def fetch_median_of_three_as_pivot(array, left, right):	
	middle = (right - left) / 2 + left
	if array[left] >= array[middle]:
		if array[left] <= array[right]:
			return array[left]
		else:
			if array[middle] > array[right]:
				swap(array, left, middle)
				return array[left]
			else:
				swap(array, right, left)
			return array[left]
	else:
		if array[left] >= array[right]:
			return array[left]
		else:
			if array[middle] < array[right]:
				swap(array, middle, left)
			else:
				swap(array, right, left)
			return array[left]
	

def swap(array, idx, idy):
	temp = array[idx]
	array[idx] = array[idy]
	array[idy] = temp

def partition_and_count(array, left, right, fetch_pivot):
	if left >= right:
		return 0
	pivot = fetch_pivot(array, left, right)
	i = left + 1
	for j in range(left + 1, right+1):
		if array[j] > pivot:
			continue
		else:
			swap(array, i, j)
			i += 1
	swap(array, left, i-1)
	comarision_count = count_each_comparision(right - left + 1)
	comarision_count += partition_and_count(array, left, i-2, fetch_pivot)
	comarision_count += partition_and_count(array, i, right, fetch_pivot)
	return comarision_count


if __name__ == '__main__':
    ints = loadIntegers("QuickSort.txt")
    left = 0
    right = len(ints) - 1
    print "fist pivot: ", partition_and_count(ints, left, right, fetch_1st_as_pivot)

    ints = loadIntegers("QuickSort.txt")
    left = 0
    right = len(ints) - 1
    print "last pivot: ", partition_and_count(ints, left, right, fetch_final_as_pivot)

    ints = loadIntegers("QuickSort.txt")
    left = 0
    right = len(ints) - 1
    print "median_of_three pivot: ", partition_and_count(ints, left, right, fetch_median_of_three_as_pivot)
    
