class Heap:
    def __init__(self, compare=None, is_max=False):
        self._array = []
        self._size = 0
        self._isMax = is_max
        if compare:
            self._compare = compare
        else:
            def compare_int(x, y):
                if x < y:
                    return -1
                elif x > y:
                    return 1
                else:
                    return 0
            self._compare = compare_int

    def size(self):
        return self._size

    def extract_top(self):
        if not self._array:
            return None
        return self._array[0]

    def pop_top(self):
        if not self._array:
            return None
        ret = self._array[0]
        self.delete_top()
        return ret

    def delete_top(self):
        self._array[0] = self._array[self._size - 1]
        del self._array[self._size - 1]
        self._size -= 1
        self._bubble_down_()

    def insert(self, v):        
        self._array.append(v)
        self._size += 1
        self._bubble_up_()

    def _swap_(self, i, j):
        temp = self._array[i]
        self._array[i] = self._array[j]
        self._array[j] = temp


    def _def_down_next_(self, cur_i):
    	left_i = 2 * cur_i + 1
        right_i = 2 * cur_i + 2
        if right_i < self._size:
            left = self._array[left_i]
            right = self._array[right_i]
            if not self._isMax:
                if self._compare(left, right) < 0:
                    next_i = left_i
                else:
                    next_i = right_i
            else:
                if self._compare(left, right) > 0:
                    next_i = left_i
                else:
                    next_i = right_i
        elif left_i >= self._size:
        	return self._size
        else:
            next_i = left_i
        return next_i

    def _bubble_down_(self):
        if not self._array:
            return
        cur_i = 0
        next_i = self._def_down_next_(cur_i)
        while next_i < self._size and \
                ((self._isMax and self._compare(self._array[next_i], self._array[cur_i]) > 0) or \
                         ((not self._isMax) and self._compare(self._array[next_i], self._array[cur_i]) < 0)):
			self._swap_(cur_i, next_i)
			cur_i = next_i
			next_i = self._def_down_next_(cur_i)


    def _bubble_up_(self):
        if not self._array:
            return
        cur_i = self._size - 1
        next_i = (cur_i - 1) / 2
        while next_i >= 0 and \
                (( (not self._isMax) and self._compare(self._array[next_i], self._array[cur_i]) > 0) or \
                         (self._isMax and self._compare(self._array[next_i], self._array[cur_i]) < 0)):
            self._swap_(cur_i, next_i)
            cur_i = next_i
            next_i = (cur_i - 1) / 2

    def __str__(self):
        return str(self._array)

    def __repr__(self):
        return str(self._array)


if __name__ == '__main__':
    def str_len_compare(x, y):
        if len(x) < len(y):
            return -1
        elif len(x) > len(y):
            return 1
        else:
            return 0

    h = Heap(str_len_compare, is_max=True)
    h.insert("1")
    print h
    h.insert("1234")
    print h
    h.insert("12")
    print h
    h.insert("12345")
    print h
    print h.pop_top()
    print h
    h.insert("123")
    print h
    print h.pop_top()
    print h
    h.insert("456")
    print h
    print h.pop_top()
    print h







