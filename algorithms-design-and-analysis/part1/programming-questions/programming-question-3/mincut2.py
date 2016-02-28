import random
from copy import deepcopy
import time, timeit


def read_file(filename):
	adjacent_dict={}  
	with open(filename) as f:
		for line in f.readlines():  
			line_num = [int(x) for x in line.split()]  
			adjacent_dict[line_num[0]]=set(line_num[1:])      
	return adjacent_dict

def fetch_edges(adjacent_dict):
	edges=[]  
	for [v1,v2_set] in adjacent_dict.items():
		edges.extend([[v1,v2] for v2 in v2_set]) 
	return edges

def random_edge_index(edges):	
	millis = int(round(time.time() * 1000))
	random.seed(millis)
	edge_no = random.randint(0, len(edges) - 1)
	return edge_no

def remove_edge(edges, edge):
	[v1, v2] = edge
	removed = []
	changed_left = []
	changed_right = []
	for idx,e in enumerate(edges):
		if e == [v1, v2] or e == [v2,v1]:
			removed.append(e)
			continue
		if e[0] == v2:
			changed_left.append(idx)
		if e[1] == v2:
			changed_right.append(idx)	

	for idx in changed_left:
		edges[idx][0] = v1

	for idx in changed_right:
		edges[idx][1] = v1

	for r in removed:
		edges.remove(r)
		
def remove_vertex(adjacent_vertex, edge):
	[v1, v2] = edge
	if v2 in adjacent_vertex[v1]:
		adjacent_vertex[v1].remove(v2)
		if v2 in adjacent_vertex:
			adjacent_vertex[v1] = adjacent_vertex[v1] | adjacent_vertex[v2]
	for v in adjacent_vertex:
		if v == v1:
			continue
		if v2 in adjacent_vertex[v]:
			adjacent_vertex[v].remove(v2)
			adjacent_vertex[v].add(v1)
	if v2 in adjacent_vertex:
		del adjacent_vertex[v2]

def contract(adjacent_vertex, edges):		
	while len(adjacent_vertex) > 2:
		contract_edge_index = random_edge_index(edges)
		edge = edges.pop(contract_edge_index)
		remove_edge(edges, edge)
		remove_vertex(adjacent_vertex, edge)
	return len(edges) / 2

		
if __name__ == '__main__':
	start = timeit.default_timer()
	filename = 'kargerMinCut.txt'
	adjacent_dict = read_file(filename)
	edges = fetch_edges(adjacent_dict)
	try_times = 200
	min_cuts = None	
	while try_times > 0:
		cuts = contract(deepcopy(adjacent_dict), deepcopy(edges))
		if not min_cuts or min_cuts > cuts:
			min_cuts = cuts
		try_times -= 1	
	stop = timeit.default_timer()
	print "contraction", try_times,"times elaplse:", stop - start
	print "number of min cuts:",min_cuts

	
	
	

