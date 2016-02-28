import random
from time import clock


def read_file(filename):
    adjacent_dict = {}
    with open(filename) as f:
        for line in f.readlines():
            line_num = [int(x) for x in line.split()]
            if adjacent_dict.get(line_num[0]) == None:
                adjacent_dict[line_num[0]] = set()
            adjacent_dict[line_num[0]].add(line_num[1])
    return adjacent_dict


class SCC:
    def __init__(self, filename, nodeNum=None):
        adjacent_dict = read_file(filename)
        self.graphic = adjacent_dict
        if nodeNum:
            self.n = nodeNum
        else:
            self.n = self._calc_nodes_num_(adjacent_dict)

    def _calc_nodes_num_(self, graphic):
        s = set()
        for k, v in graphic.items():
            s.add(k)
            s |= v
        return len(s)

    def scc_by_recursive(self):
        all_nodes = range(1, self.n + 1)
        inv_g = self._inverse_graphic_(self.graphic)
        inv_f, leader_dict = self._dfs_loop_(inv_g, all_nodes)
        order_nodes = self._sort_finish_time_(inv_f)
        inv_f, leader_dict = self._dfs_loop_(self.graphic, order_nodes)
        ret = self._order_max_5_scc_(leader_dict)
        print ret
        return ret

    def scc_by_loop(self):
        all_nodes = range(1, self.n + 1)
        # random.shuffle(all_nodes)
        inv_g = self._inverse_graphic_(self.graphic)
        inv_f, leader_dict = self._dfs_loop_iterative_(inv_g, all_nodes)
        order_nodes = self._sort_finish_time_(inv_f)
        inv_f, leader_dict = self._dfs_loop_iterative_(self.graphic, order_nodes)
        ret = self._order_max_5_scc_(leader_dict)
        print ret
        return ret

    def _init_scc_(self):
        self.explored = [False] * (self.n + 1)
        self.finish_time = 0
        self.finish_dict = [0] * (self.n + 1)
        self.leader = 0
        self.leader_dict = [0] * (self.n + 1)

    def _sort_finish_time_(self, finish_dict):
        magic_order_nodes = [0] * self.n
        for node, order in enumerate(finish_dict[1:]):
            magic_order_nodes[self.n - order] = node + 1
        return magic_order_nodes

    def _dfs_loop_iterative_(self, graphic, nodes):
        self._init_scc_()
        for v in nodes:
            if not self.explored[v]:
                self.leader = v
                self._dfs_iter_(graphic, v)
        return self.finish_dict, self.leader_dict

    def _dfs_iter_(self, graphic, s):
        search_list = {}
        cur = s
        visited = []
        while cur:
            if search_list.get(cur) == None:
                search_list[cur] = []
            if not self.explored[cur]:
                self.explored[cur] = True
                # mark s's leader
                self.leader_dict[cur] = self.leader
                if graphic.get(cur):
                    for v in graphic[cur]:
                        if not self.explored[v]:
                            search_list[cur].append(v)
            if not search_list[cur]:
                if self.finish_dict[cur] == 0:
                    self.finish_time += 1
                    # mark s's finish time
                    self.finish_dict[cur] = self.finish_time
                if visited:
                    cur = visited.pop()
                else:
                    cur = None
            else:
                visited.append(cur)
                cur = search_list[cur].pop()

    def _dfs_loop_(self, graphic, nodes):
        self._init_scc_()
        for v in nodes:
            if not self.explored[v]:
                self.leader = v
                self._dfs_(graphic, v)
        return self.finish_dict, self.leader_dict

    def _dfs_(self, graphic, s):
        self.explored[s] = True
        # mark s's leader
        self.leader_dict[s] = self.leader
        if graphic.get(s):
            for v in graphic[s]:
                if self.explored[v]:
                    continue
                self._dfs_(graphic, v)
        self.finish_time += 1
        # mark s's finish time
        self.finish_dict[s] = self.finish_time


    def _inverse_graphic_(sef, graphic):
        inv_g = {}
        for v, edages in graphic.items():
            for e in edages:
                if inv_g.get(e) == None:
                    inv_g[e] = set()
                inv_g[e].add(v)
        return inv_g

    def _order_max_5_scc_(self, leader_dict):
        d = {}
        for node, group in enumerate(leader_dict[1:]):
            if d.get(group) == None:
                d[group] = 0
            d[group] += 1
        templist = [[v, k] for k, v in d.items()]
        templist.sort(reverse=True)
        ret = []
        if len(templist) >= 5:
            ret = [v[0] for v in templist[0:5]]
        else:
            ret = [v[0] for v in templist]
            if len(ret) < 5:
                ret += [0] * (5 - len(ret))
        return ','.join([str(i) for i in ret])


def test():
    test_files = ['SCC.sim1.txt', 'SCC.sim2.txt', 'SCC.sim3.txt', 'SCC.sim4.txt', 'SCC.sim5.txt', ]
    result_files = ['SCC.ret1.txt', 'SCC.ret2.txt', 'SCC.ret3.txt', 'SCC.ret4.txt', 'SCC.ret5.txt', ]
    ret = True
    for i in range(len(test_files)):
        s1 = SCC(test_files[i]).scc_by_loop()
        with open(result_files[i]) as f:
            s2 = f.readline().strip()
        print "algo:", str(s1)
        print "act:", str(s2)
        print
        if s1 != s2:
            ret = False
    return ret


def scc_recursive():
    import sys, threading

    sys.setrecursionlimit(3000000)
    threading.stack_size(64 * 1024 * 1024)  # set thread stack 64M
    start = clock()
    thread = threading.Thread(target=SCC("SCC.txt", nodeNum=875714).scc_by_recursive)
    thread.start()
    thread.join()
    end = clock()
    print "run by recursion:", str(end - start)


def scc_loop():
    start = clock()
    SCC("SCC.txt", nodeNum=875714).scc_by_loop()
    end = clock()
    print "run by for-loop:", str(end - start)


if __name__ == '__main__':
    ret = test()
    if not ret:
        print "algo wrong"
        exit(0)

    scc_loop()

    scc_recursive()



