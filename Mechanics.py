__author__ = "Vivek Kumar"
import numpy as np

'''Columns and Rows'''
column_number = None
row_number = None

'''Goal Position'''
gpos = (None,None) #As indexes, (1,6)

def read(level):
    '''
    Takes text encoding and returns matrix representation of state.
    We assume that the matrix is rectangular.
    '''
    levString = level.read()
    split = levString.split('\n')
    for (index,item) in enumerate(split):
        if item == '#' * len(item):
            split.pop(index)
    split.pop(-1)

    cutIndex1 = 0
    cutIndex2 = 0
    levelMatrix = []

    for row in split:
        matrow = []
        for (index,character) in enumerate(row):
            matrow.append(character)
            if character == "+":
                cutIndex1 = index
                continue
            if character == "*":
                cutIndex2 = index
                continue
            else:
                pass
        levelMatrix.append(matrow)

    goal_Row = 1 #Marks row of goal position
    for row in levelMatrix:
        goal_Column = 0 #Marks column of goal position
        for (index, character) in enumerate(row):
            if character == "+":
                row[index+1] = 2
                goal_Column += 1
            if character == ".":
                row[index] = 0
                goal_Column += 1
            if character == "L" or character == "R" or character == "C":
                row[index] = 1
                goal_Column += 1
            if character == "*":
                goal_Pos = (goal_Row,goal_Column)
        goal_Row += 1

    state = []
    for i in range(len(levelMatrix)):
        state.append(levelMatrix[i][cutIndex1+1:cutIndex2])

    final_state = np.array(state)
    return (final_state, goal_Pos)

def matrix_shape(matrix):
    '''
    Returns column and row number of matrix.
    '''
    return (matrix.shape[0],matrix.shape[1])

def down(matrix_representation, LCFS=False):
    '''
    Moves the character down, if possible.
    '''
    column_counter = 0
    while column_counter < column_number:
        row_counter = 0
        while row_counter < row_number:
            if matrix_representation[row_counter][column_counter] == 2:
                if row_counter + 1 < row_number and matrix_representation[row_counter+1][column_counter] != 1:
                    matrix_representation[row_counter+1][column_counter] = 2
                    matrix_representation[row_counter][column_counter] = 0
                    if LCFS == False:
                        return matrix_representation
                    else:
                        return (0,matrix_representation)
            row_counter += 1
        column_counter += 1
    return None

def up(matrix_representation, LCFS=False):
    '''
    Moves the character up, if possible.
    '''
    column_counter = 0
    while column_counter < column_number:
        row_counter = 0
        while row_counter < row_number:
            if matrix_representation[row_counter][column_counter] == 2:
                if (row_counter - 1 < 0) == False and matrix_representation[row_counter - 1][column_counter] != 1:
                    matrix_representation[row_counter - 1][column_counter] = 2
                    matrix_representation[row_counter][column_counter] = 0
                    if LCFS == False:
                        return matrix_representation
                    else:
                        return (0,matrix_representation)
            row_counter += 1
        column_counter += 1
    return None

def right(matrix_representation,LCFS=False):
    '''
    Moves the character right, if possible
    '''
    for row in range(row_number):
        for column in range(column_number):
            if matrix_representation[row][column] == 2:
                if (column + 1) == column_number or (matrix_representation[row][-1] == 1 and matrix_representation[row][column+1] == 1):
                    return None
                elif matrix_representation[row][column+1] == 0:
                    matrix_representation[row][column] = 0
                    matrix_representation[row][column+1] = 2
                    if LCFS == False:
                        return matrix_representation
                    else:
                        return (0,matrix_representation)
                elif matrix_representation[row][column+1] == 1:
                    newrow = np.roll(matrix_representation[row],1) #Rotates array
                    matrix_representation[row] = newrow
                    if LCFS == False:
                        return matrix_representation
                    else:
                        return (1,matrix_representation)
    return None

def left(matrix_representation,LCFS=False):
    '''
    Moves the character left, if possible.
    '''
    for row in range(row_number):
        for column in range(column_number):
            if matrix_representation[row][column] == 2:
                if (column - 1) < 0 or (matrix_representation[row][0] == 1 and matrix_representation[row][column-1] == 1):
                    return None
                elif matrix_representation[row][column-1] == 0:
                    matrix_representation[row][column] = 0
                    matrix_representation[row][column-1] = 2
                    if LCFS == False:
                        return matrix_representation
                    else:
                        return (0,matrix_representation)
                elif matrix_representation[row][column-1] == 1:
                    newrow = np.roll(matrix_representation[row],-1) #Rotates array
                    matrix_representation[row] = newrow
                    if LCFS == False:
                        return matrix_representation
                    else:
                        return (1,matrix_representation)
    return None

def neighbors(vertex, LCFS=False):
    '''
    Makes 4 copies of vertex, and runs each function on them. Returns if successful.
    If LCFS is True, then a neighbor_list will be a list of tuples.
    '''
    if LCFS == False:
        neighbor_list = []
        v1 = np.copy(vertex)
        v2 = np.copy(vertex)
        v3 = np.copy(vertex)
        v4 = np.copy(vertex)
        if up(v1) is not None:
            neighbor_list.append(v1)
        if down(v2) is not None:
            neighbor_list.append(v2)
        if right(v3) is not None:
            neighbor_list.append(v3)
        if left(v4) is not None:
            neighbor_list.append(v4)
        return neighbor_list

    elif LCFS == True:
        neighbor_list1 = []
        v5 = np.copy(vertex)
        v6 = np.copy(vertex)
        v7 = np.copy(vertex)
        v8 = np.copy(vertex)
        vfake1 = np.copy(v5)
        vfake2 = np.copy(v6)
        vfake3 = np.copy(v7)
        vfake4 = np.copy(v8)
        if up(vfake1) is not None:
            neighbor_list1.append(up(v5,True))
        if down(vfake2) is not None:
            neighbor_list1.append(down(v6,True))
        if right(vfake3) is not None:
            neighbor_list1.append(right(v7,True))
        if left(vfake4) is not None:
            neighbor_list1.append(left(v8,True))
        return neighbor_list1


def is_goal(A):
    '''
    Tests for goal.
    '''
    return A[gpos[0]-1][gpos[1]-1] == 2

def cost(path):
    '''
    Finds the total cost of a path.
    '''
    cost = 0
    newpath = []
    for item in path:
        cost += item[0]
        newpath.append(item[-1])
    return (cost, newpath)
