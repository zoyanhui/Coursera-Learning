def read_file(filename):
    adjacent_dict = {}
    with open(filename) as f:
        for line in f.readlines():
            splits = [x for x in line.split()]
            v = int(splits[0])
            if adjacent_dict.get(v) == None:
                adjacent_dict[v] = {}
            edge_values = [x.split(',') for x in splits[1:]]
            for e in edge_values:
            	adjacent_dict[v][int(e[0])] = int(e[1])
    return adjacent_dict

def calc_nodes_num(adjacent_dict):
    s = set()
    for k, v in adjacent_dict.items():
        s.add(k)
        s |= set(v.keys())
    return len(s)


# naive dijkstra algorithm, O(mn)
def naive_dijkstra(adjacent_dict, s=1, n=None):
	if n == None:
		n = calc_nodes_num(adjacent_dict)
	path_len = {s:0}
	path = {s:[s,]}
	Xset = set((s,))
	cur_w = s
	while len(Xset) < n and cur_w:
		# update path_len of vertex connected from cur_w
		if adjacent_dict.get(cur_w) != None:
			for node, edge_len in adjacent_dict[cur_w].items():
				node_len = path_len[cur_w] + edge_len
				if path_len.get(node) == None or node_len < path_len[node]:
					path_len[node] = node_len
					path[node] = path[cur_w] + [node,]		
		# find next cur_w
		min_node = None
		min_node_val = None
		for node, plen in path_len.items():
			if node in Xset:
				continue
			if (not min_node_val) or (min_node_val > plen):
				min_node_val = plen
				min_node = node
		Xset.add(min_node)
		cur_w = min_node
	return path_len, path


# dijkstra algorithm by heap, O(mlogn)
def adv_dijkstra(adjacent_dict, s=1, n=None):
	if n == None:
		n = calc_nodes_num(adjacent_dict)
	from nodeHeap import NodeHeap
	path_len = {s:0}
	path = {s:[s,]}
	Xset = set((s,))
	sel_heap = NodeHeap()
	cur_w = s
	while len(Xset) < n and cur_w:
		# update path_len of vertex connected from cur_w
		if adjacent_dict.get(cur_w) != None:
			for node, edge_len in adjacent_dict[cur_w].items():
				sel_heap.delete(node)
				node_len = path_len[cur_w] + edge_len
				if path_len.get(node) == None or node_len < path_len[node]:
					path_len[node] = node_len
					path[node] = path[cur_w] + [node,]
				if node not in Xset:				
					sel_heap.insert([node, path_len[node]])	
		# find next cur_w
		min_node, min_node_val = sel_heap.pop_top()
		if min_node != None:		
			Xset.add(min_node)
			sel_heap.delete(min_node)
		cur_w = min_node					
	return path_len, path


def print_result(path_len, ret_node):
	ret = None
	if not ret_node:
		ret_node = path_len.keys()
	for n in ret_node:
		s = "1000000"
		if path_len.get(n) != None:
			s = str(path_len[n])
		if ret:
			ret = ret + "," + s
		else:
			ret = s
	print ret
	return ret

def test():
	test_files = ['test_case1.txt', 'test_case2.txt', 'test_case3.txt',]
	result_files = ['test_case_ret1.txt', 'test_case_ret2.txt', 'test_case_ret3.txt', ]
	ret = True
	for i in range(len(test_files)):
		s1 = run_main_adv(test_files[i], ret_node = None, n=None)
		with open(result_files[i]) as f:
			s2 = f.readline().strip()
		print "algo:", str(s1)
		print "act:", str(s2)
		print
		if s1 != s2:
			ret = False
	return ret

def run_main(filename, ret_node, n=None):
	adjacent_dict = read_file(filename)
	path_len, path = naive_dijkstra(adjacent_dict, s = 1, n=n)
	return print_result(path_len, ret_node)

def run_main_adv(filename, ret_node, n=None):
	adjacent_dict = read_file(filename)
	path_len, path = adv_dijkstra(adjacent_dict, s = 1, n=n)
	return print_result(path_len, ret_node)


if __name__ == '__main__':	
	test()
	ret_node = [7,37,59,82,99,115,133,165,188,197]
	print "naive dijkstra:"
	run_main('dijkstraData.txt', ret_node, n = 200)
	print "dijkstra by heap:"
	run_main_adv('dijkstraData.txt', ret_node, n = 200)

