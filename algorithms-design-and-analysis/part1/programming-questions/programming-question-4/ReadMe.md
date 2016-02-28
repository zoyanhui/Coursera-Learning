# SCC(strongly connected components) Problem, Solved by recursion call or for-loop  
The SCC problem are solved by two way, one is recursive call, another is for-loop.  
The implementation of for-loop by *Python* does not need `setrecursionlimit`.

## Problem Instruction    
The txt file contains the edges of a directed graph. Vertices are labeled as positive integers from 1 to 875714. Every row indicates an edge, the vertex label in first column is the tail and the vertex label in second column is the head (recall the graph is directed, and the edges are directed from the first column vertex to the second column vertex). So for example, the 11th row looks liks : "2 47646". This just means that the vertex with label 2 has an outgoing edge to the vertex with label 47646  

Your task is to code up the algorithm from the video lectures for computing strongly connected components (SCCs), and to run this algorithm on the given graph.  

Output Format: You should output the sizes of the 5 largest SCCs in the given graph, in decreasing order of sizes, separated by commas (avoid any spaces). So if your algorithm computes the sizes of the five largest SCCs to be 500, 400, 300, 200 and 100, then your answer should be "500,400,300,200,100". If your algorithm finds less than 5 SCCs, then write 0 for the remaining terms. Thus, if your algorithm computes only 3 SCCs whose sizes are 400, 300, and 100, then your answer should be "400,300,100,0,0".

## Data Instruction  
*original data*: txt file is SCC.txt and zip data file is SCC.zip.  
*test data*: SCC.sim*.txt and SCC.ret*.txt is the test data and test result.  

**algorithm code in SCC.py**  
recursion solution: `scc_recursive()`  
for-loop solution: `scc_loop()`

**test**  
test by test method `test()`
*Result:*  
```
(3, 3, 3)
['3,3,3,0,0\n']

(3, 3, 2)
['3,3,2,0,0\n']

(3, 3, 1, 1)
['3,3,1,1,0\n']

(7, 1)
['7,1,0,0,0\n']

(6, 3, 2, 1)
['6,3,2,1,0\n']
```  

## Reference
[Coursera](https://www.coursera.org/) course, [Algorithms: Design and Analysis, Part 1](https://class.coursera.org/algo-009/),Programming problem, [Programming Question-4](https://class.coursera.org/algo-009/quiz/attempt?quiz_id=57)
