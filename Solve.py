__author__ = "Vivek Kumar"
import Mechanics as m
import numpy as np

def BFS(start):
    '''
    Breadth-First Search
    Utilizes the frontier as a queue.
    '''
    frontier = []
    frontier.append([start])
    while len(frontier) > 0:
        path = frontier.pop(0)
        last_vertex = path[-1]
        if m.is_goal(last_vertex):
            return path
        for next_vertex in m.neighbors(last_vertex):
            new_path = path + [next_vertex]
            frontier.append(new_path)
    return None

def DFS(start):
    '''
    Depth-First Search
    Utilizes the frontier as a stack.
    Unfortunately this will often fall into cycles.
    '''
    frontier = []
    frontier.append([start])
    while len(frontier) > 0:
        path = frontier.pop() #Removing the zero turns our queue into a stack.
        last_vertex = path[-1]
        if is_goal(last_vertex):
            return path
        for next_vertex in neighbors(last_vertex):
            new_path = path + [next_vertex]
            frontier.append(new_path)
    return None

def DFS_Enhanced(start):
    '''
    Enhanced Depth-First-Search with cycle detection and path pruning.
    Checks if the vertex is already in the path, or already on another path.s
    '''
    frontier = []
    frontier.append([start])
    while len(frontier) > 0:
        path = frontier.pop()
        last_vertex = path[-1]
        if m.is_goal(last_vertex):
            return path
        for next_vertex in m.neighbors(last_vertex):
            multpath = False
            for member in frontier: #Checks if the new vertex is on any previous path. If so, discard path.
                if any((next_vertex == x).all() for x in member):
                    multpath = True
                    break
            if multpath == True:
                continue
            if any((next_vertex == x).all() for x in path): #If new vertex already in path, ignore this neighbor.
                continue
            else:
                new_path = path + [next_vertex]
                frontier.append(new_path)
    return None

def DFS_bound(start,depth):
    '''
     Depth = Max number of moves to solve problem, using cycle detection and path pruning
     If the length of the path is past a maximum depth, the function will cease to increase this path.
     '''
    frontier = []
    frontier.append([start])
    while len(frontier) > 0:
        path = frontier.pop()
        last_vertex = path[-1]
        if m.is_goal(last_vertex):
            return path
        if (len(path)) == depth: #Discard path if more than depth steps and the end vertex is not a goal
            continue
        for next_vertex in m.neighbors(last_vertex):
            multpath = False
            for member in frontier:
                if any((next_vertex == x).all() for x in member):
                    multpath = True
                    break
            if multpath == True:
                continue
            if any((next_vertex == x).all() for x in path):
                continue
            else:
                new_path = path + [next_vertex]
                frontier.append(new_path)
    return None

def Deep(start):
    '''
    Iterative Deepening, "continuously bounds" the size of the path.
    This is a depth-first search algorithm with a bound on each attempt.
    '''
    max_length = 0
    frontier = []
    while True:
        if len(frontier) == 0: #Increases allowed path length
            max_length += 1
            frontier.append([start])
        path = frontier.pop()
        last_vertex = path[-1]
        if m.is_goal(last_vertex):
            return path
        if len(path) == max_length: #Prevents moving further than allowed path length.
            continue
        for next_vertex in m.neighbors(last_vertex):
            multpath = False
            for member in frontier:
                if any((next_vertex == x).all() for x in member):
                    multpath = True
                    break
            if multpath == True:
                continue

            if any((next_vertex == x).all() for x in path):
                continue
            else:
                new_path = path + [next_vertex]
                frontier.append(new_path)
    return None

def LCFS(start):
    '''
    Finds the path of least cost. We do this by iteratively increasing the cost each iteration of the loop.
    '''
    allowed_cost = 0
    frontier = []
    while True:
        if len(frontier) == 0: #Increases allowed cost
            allowed_cost += 1
            frontier.append([(0,start)])
        path = frontier.pop(0) #We implement the frontier as a queue.
        last_vertex = path[-1]
        if m.is_goal(last_vertex[-1]):
            return (m.cost(path), path)
        if m.cost(path)[0] == allowed_cost: #Prevents moving further than allowed cost.
            continue
        for next_vertex in m.neighbors(last_vertex[-1], True):
            multpath = False
            for member in frontier:
                if any((next_vertex[-1] == x[-1]).all() for x in member):
                    multpath = True
                    break
            if multpath == True:
                continue
            if any((next_vertex[-1] == x[-1]).all() for x in path):
                continue
            else:
                new_path = path + [next_vertex]
                frontier.append(new_path)
    return None


if __name__ == "__main__":
    #Simply comment out any functions you don't want to write output.

    #Prints the level
    print "\nVERTEX"
    level = open("Level.txt",'r') #PATH TO FILE
    (lev3,goal) = m.read(level)
    print lev3


    #Obtains number of columns, rows, and goal for mechanics functions
    m.column_number = m.matrix_shape(lev3)[1]
    m.row_number = m.matrix_shape(lev3)[0]
    m.gpos = goal

    #BFS often takes time to get to the solution, so we can manually move the person closer to test BFS.
    print "\nBFS"
    test = np.array([[1,1,2,0,1,1,0],[0,1,0,1,0,1,0],[1,1,0,1,0,0,0]])
    path = BFS(test)
    for vertex in path:
        print "\n"
        print vertex

    #Finds the lowest cost solution
    print "\nLCFS"
    path = LCFS(lev3)
    print "Cost: " + str(path[0][0])
    for vertex in path[0][-1]:
        print "\n"
        print vertex

    #Tests DFS_Enhanced because DFS often gets into cycles.
    print "\nDFS_ENHANCED"
    path = DFS_Enhanced(lev3)
    for vertex in path:
        print "\n"
        print vertex

    #Places bound on DFS.
    print "\nDFS_BOUND"
    path = DFS_bound(lev3,40) #Currently return solution of size 38. Making bound smaller returns solution of size 36, unless bound is made less than 36.
    if path is not None:
        for (i, vertex) in enumerate(path):
            print "\n"
            print i+1
            print vertex
    else:
        print "No solution in given bound"

    #Iterative Deepening (Will always find the minimum solution, should match DFS_Bound with minimum bound of 36). Also, this is somewhat slow.
    print "\nITERATIVE DEEPENING"
    path = Deep(lev3)
    for (i, vertex) in enumerate(path):
        print "\n"
        print i + 1
        print vertex
