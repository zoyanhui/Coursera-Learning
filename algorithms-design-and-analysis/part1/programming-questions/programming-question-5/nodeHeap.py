class NodeHeap:
	# node defined by int[] of two elements [node, score]

	def __init__(self):
		self._array = []
		self._size = 0
		self._nodemap = {}
		def compare_node(x, y):
			if x[1] < y[1]:
				return -1
			elif x[1] > y[1]:
				return 1
			else:
				return 0
		self._compare = compare_node

	def extract_min(self):
		if not self._array:
			return None
		return self._array[0]

	def pop_top(self):
		if not self._array:
			return None,None
		ret = self._array[0]
		self.delete_top()
		return ret

	def delete_top(self):
		if self._size == 0:
			return
		pos = 0
		self._swap_(pos, self._size - 1)
		del self._nodemap[self._array[self._size - 1][0]]
		del self._array[self._size - 1]		
		self._size -= 1
		self._bubble_down_(pos)

	def insert(self, v):
		self._array.append(v)
		self._nodemap[v[0]] = self._size
		self._size += 1
		self._bubble_up_()

	def delete(self, node):
		pos = self._nodemap.get(node,None)
		if pos == None:
			return
		self._swap_(pos, self._size - 1)
		del self._nodemap[self._array[self._size - 1][0]]
		del self._array[self._size - 1]
		self._size -= 1
		self._bubble_down_(pos)

	def _swap_(self, i, j):
		def _swap_node_map_(nodei, nodej):
			temp = self._nodemap[nodei]
			self._nodemap[nodei] = self._nodemap[nodej]
			self._nodemap[nodej] = temp
		_swap_node_map_(self._array[i][0], self._array[j][0])
		temp = self._array[i]
		self._array[i] = self._array[j]		
		self._array[j] = temp	
		
	def _def_down_next_(self, cur_i):
		left_i = 2 * cur_i + 1
		right_i = 2 * cur_i + 2
		if right_i < self._size:
			left = self._array[left_i]
			right = self._array[right_i]			
			if self._compare(left, right) < 0:
				next_i = left_i
			else:
				next_i = right_i
			
		elif left_i >= self._size:
			return self._size
		else:
			next_i = left_i
		return next_i
 
	def _bubble_down_(self, pos):
		if not self._array:
			return
		cur_i = pos
		next_i = self._def_down_next_(cur_i)
		while next_i < self._size and self._compare(self._array[next_i], self._array[cur_i]) < 0:
			self._swap_(cur_i, next_i)
			cur_i = next_i
			next_i = self._def_down_next_(cur_i)


	def _bubble_up_(self):
		if not self._array:
			return
		cur_i = self._size - 1
		next_i = (cur_i - 1) / 2		
		while next_i >=0 and self._compare(self._array[next_i], self._array[cur_i]) > 0:
			self._swap_(cur_i, next_i)
			cur_i = next_i
			next_i = (cur_i - 1) / 2

	def __str__(self):
		return str(self._array) + "\n" + str(self._nodemap) +"\n"

	def __repr__(self):
		return str(self._array)




if __name__ == '__main__':
	h = NodeHeap()
	h.insert([1,1])
	print h
	h.insert([3,3])
	print h
	h.insert([2,2])
	print h
	h.insert([4,4])
	print h
	print h.delete(3)
	print h
	h.insert([3,0])
	print h
	h.insert([5,5])
	print h
	print h.delete(5)
	print h
	h.insert([5,3])
	print h
	h.insert([6,2])
	print h
	print h.delete(1)
	print h







