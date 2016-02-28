import random
import time

class Vertex:	
	def __init__(self, num):
		self._num = num
		self._con_vertexs = {}					

	def conncet_to(self, otherVertex, edge_num = 1):
		en = self._con_vertexs.get(otherVertex)
		if not en:
			en = 0
		en += edge_num
		self._con_vertexs[otherVertex] = en

	def delete_connect(self, otherVertex):
		if self._con_vertexs.get(otherVertex):
			del self._con_vertexs[otherVertex]

	def edge_num(self):
		num = 0
		for v,n in self._con_vertexs.items():
			num += n
		return num

	def connect_vertexs(self):
		return self._con_vertexs

	def add_edges(self, total_edge_dict):		
		for v,n in self._con_vertexs.items():
			e = Edge(self, v)
			if total_edge_dict.get(e):
				continue			
			total_edge_dict[Edge(self, v)] = n				

	def get_num(self):
		return self._num

	def combine(self, otherVertex):
		en = self._con_vertexs.get(otherVertex)
		if not en:
			return
		for v,n in otherVertex.connect_vertexs().items():
			if v == self:
				continue
			self.conncet_to(v, n)
			# delete combined and reconnect to new
			v.conncet_to(self, n)
			v.delete_connect(otherVertex)

		if self._con_vertexs.get(otherVertex):
			del self._con_vertexs[otherVertex]
		# delete self circle edge
		if self._con_vertexs.get(self):
			del self._con_vertexs[self]

	def __str__(self):
		return str(self._num)

	def __repr__(self):
		return str(self._num)

	def __eq__(self, other):
		return self._num == other._num

	def __hash__(self):
		return hash(self._num)


class Edge:
	def __init__(self, vertex1, vertex2):
		self._vertexs = set()
		self._vertexs.add(vertex1)
		self._vertexs.add(vertex2)

	def vertexs(self):
		return tuple(self._vertexs)

	def __eq__(self, other):
		return self._vertexs == other._vertexs

	def __hash__(self):
		return hash(tuple(self._vertexs))

	def __str__(self):
		if not self._vertexs:
			return ''
		vs = tuple(self._vertexs)
		return str(vs[0])+"-"+str(vs[1])

	def __repr__(self):
		if not self._vertexs:
			return ''
		vs = tuple(self._vertexs)
		return str(vs[0])+"-"+str(vs[1])


def combine_vertex(vertex_list, vertex1, vertex2):
	vertex1.combine(vertex2)
	vertex_list.remove(vertex2)
	del vertex2

def read_file(filename, n):
	with open(filename) as f:
		content = f.readlines()
	if not content:
		return None
	array = []
	for v in range(1,n+1):
		vertex = Vertex(v)
		array.append(vertex)

	for line in content:
		line = line.strip()
		if len(line) ==0:
			continue
		nums = line.split("\t")
		if len(nums) ==0:
			continue
		vertex = array[int(nums[0]) - 1]
		for v in nums[1:]:
			if not v:
				continue
			v = v.strip()
			if len(v) > 0:
				vertex.conncet_to(array[int(v) - 1])
	return array

def random_edge(vertex_list):
	total_edges = fetch_total_edges(vertex_list)	
	millis = int(round(time.time() * 1000))
	random.seed(millis)
	edge_no = random.randint(1, len(total_edges))
	return total_edges[edge_no - 1]

def print_vertex_list(vertex_list):
	print '--------'
	for v in vertex_list:
		print str(v),
		for e,n in v.connect_vertexs().items():
			print str(e.get_num())+"("+str(n)+")",
		print
	print '########'

def fetch_total_edges(vertex_list):
	total_edges_dict = {}
	for v in vertex_list:
		v.add_edges(total_edges_dict)	
	total_edges = []
	for e,n in total_edges_dict.items():
		for i in range(0,n):
			total_edges.append(e)
	return total_edges

def do_contract(vertex_list):
	contract_edge = random_edge(vertex_list)
	contract_vertexs = contract_edge.vertexs()
	
	contract_vertexs[0].combine(contract_vertexs[1])	
	vertex_list.remove(contract_vertexs[1])	

def contract(filename, n):
	vertex_list = read_file(filename, n)	
	while len(vertex_list) > 2:
		do_contract(vertex_list)

	return len(fetch_total_edges(vertex_list)), vertex_list


if __name__ == '__main__':
	n = 200 # number of vertexs
	filename = 'kargerMinCut.txt'
	min_cuts_vertex_list = read_file(filename, n)
	print_vertex_list(min_cuts_vertex_list)
	try_times = 100
	min_cuts = n - 1	
	while try_times > 0:
		cuts,vertex_list = contract(filename, n)
		if min_cuts > cuts:
			min_cuts = cuts
			min_cuts_vertex_list = vertex_list
		try_times -= 1	
	print "after contraction"
	print_vertex_list(min_cuts_vertex_list)
	print "number of min cuts:",min_cuts
	
	
	

