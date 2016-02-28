
def loadIntegers(filename):
    with open(filename) as f:
        content = f.readlines()
    if not content:
        return None
    array = []
    for c in content:
        array.append(int(c))
    return array


def countInverse(ints, left, right):
    n = right - left + 1
    if n <= 1:
        return 0
    mid = int( (right - left) /2) + left
    left_count = countInverse(ints, left, mid)
    right_count = countInverse(ints, mid+1, right)
    count = countInverseFromLR(ints, left, right, mid)
    return left_count + count + right_count


def countInverseFromLR(ints, left, right, mid):
    n = right - left + 1
    reints = [None] * n
    i = left
    j = mid + 1
    inverseCount = 0
    k = 0
    while k <= n-1:
        if i > mid or j > right:
            break
        if(ints[i] < ints[j]):
            reints[k] = ints[i]
            i += 1
        else:
            reints[k] = ints[j]
            j += 1
            inverseCount += mid - i + 1
        k+=1
    if i > mid and j <= right:
        reints[k:] = ints[j:right + 1]
    elif j > right and i <=mid:
        reints[k:] = ints[i:mid + 1]
    k = left
    for v in reints:
        ints[k] = v
        k += 1
    return inverseCount


if __name__ == '__main__':
    ints = loadIntegers("IntegerArray.txt")
    n = len(ints)
    print countInverse(ints, 0, n - 1)
    print ints
