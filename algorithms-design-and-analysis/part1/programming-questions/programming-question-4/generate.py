# # This code is from discussion Forums of course[Algorithms: Design and Analysis, Part 1] in Coursera, by Philip Ronan·
from __future__ import print_function
import random

max_node = 1
sccs = [[1]]
edges = []


def add_scc():
    global max_node, sccs, edges
    max_node += 1
    for scc in random.sample(sccs, random.randint(1, min(3, len(sccs)))):
        edges += [[random.choice(scc), max_node]]
    sccs += [[max_node]]


def expand_scc():
    global max_node, sccs, edges
    max_node += 1
    which_scc = random.randint(0, len(sccs) - 1)
    if len(sccs[which_scc]) == 1:
        old_node = sccs[which_scc][0]
        sccs[which_scc] += [max_node]
        edges += [[old_node, max_node], [max_node, old_node]]
    else:
        (node1, node2) = random.sample(sccs[which_scc], 2)
        if edges.count([node1, node2]):
            edges.remove([node1, node2])
            edges.append([node1, max_node])
            edges.append([max_node, node2])
            sccs[which_scc].append(max_node)
        elif edges.count([node2, node1]):
            edges.remove([node2, node1])
            edges.append([node2, max_node])
            edges.append([max_node, node1])
            sccs[which_scc].append(max_node)
        else:
            edges.append([node1, max_node])
            edges.append([max_node, node2])
            sccs[which_scc].append(max_node)


def build_graph():
    global max_node, sccs, edges
    while True:
        nscc = int(raw_input('How many SCCs? '))
        if nscc >= 1:
            break
        print('Must have at least one. Try again.')
    while True:
        add_nodes = int(raw_input('How many additional nodes? '))
        if add_nodes >= 0:
            break
        print('No. Try again.')
    for i in range(nscc - 1):
        add_scc()
    for i in range(add_nodes):
        expand_scc()
    scc_sizes = [len(s) for s in sccs]
    scc_sizes.sort()
    scc_sizes.reverse()
    random.shuffle(edges)
    print('Graph created. SCC sizes are as follows:')
    print(','.join([str(s) for s in scc_sizes]))
    outfile = raw_input('Output filename: ')
    with open(outfile, 'w') as the_file:
        for e in edges:
            the_file.write(str(e[0]) + ' ' + str(e[1]) + '\n')
    print('Finished')


build_graph()