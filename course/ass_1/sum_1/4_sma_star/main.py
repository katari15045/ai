from math import sqrt
from time import time
from copy import deepcopy
from collections import deque

start_time = time()
global grid
global n, rows
global tar_conf, tar_grid
global iterations
global max_nodes, max_deque_size
global moves

class params():
    def __init__(self, grid, empty_row, empty_col, cost_so_far, path):
        self.grid = grid
        self.empty_row = empty_row
        self.empty_col = empty_col
        self.cost_so_far = cost_so_far
        self.future_cost = get_future_cost(self)
        self.total_cost = self.cost_so_far + self.future_cost
        self.path = path

def a_star():
    global n, grid, configs, rows, configs, iterations, max_deque_size, moves
    leaves = deque()
    rows = int(sqrt(n+1))
    empty_row, empty_col = get_empty_cell()
    obj = params(deepcopy(grid), empty_row, empty_col, 0, [])
    leaves.append(obj)
    while(len(leaves) > 0):
        iterations = iterations+1
        if(len(leaves) > max_deque_size):
            max_deque_size = len(leaves)
        handle_memory(leaves)
        obj = get_optimal_leaf(leaves)
        grid = obj.grid
        empty_row = obj.empty_row
        empty_col = obj.empty_col
        path = obj.path
        # Bottom Check
        if(empty_row != (rows-1)):
            grid_copy = deepcopy(grid)
            path_copy = deepcopy(path)
            swap_cells(grid_copy, empty_row+1, empty_col, empty_row, empty_col)
            if(is_dup_conf(grid_copy) == False):
                cur_conf = get_conf(grid_copy)
                path_copy.append("Down")
                if(cur_conf == tar_conf):
                    grid = grid_copy
                    moves = path_copy
                    return
                new_obj = params(grid_copy, empty_row+1, empty_col, obj.cost_so_far+1, path_copy)
                leaves.append(new_obj)
        # Top Check
        if(empty_row != 0):
            grid_copy = deepcopy(grid)
            path_copy = deepcopy(path)
            swap_cells(grid_copy, empty_row-1, empty_col, empty_row, empty_col)
            if(is_dup_conf(grid_copy) == False):
                cur_conf = get_conf(grid_copy)
                path_copy.append("Up")
                if(cur_conf == tar_conf):
                    grid = grid_copy
                    moves = path_copy
                    return
                new_obj = params(grid_copy, empty_row-1, empty_col, obj.cost_so_far+1, path_copy)
                leaves.append(new_obj)
        # Right Check
        if(empty_col != (rows-1)):
            grid_copy = deepcopy(grid)
            path_copy = deepcopy(path)
            swap_cells(grid_copy, empty_row, empty_col+1, empty_row, empty_col)
            if(is_dup_conf(grid_copy) == False):
                cur_conf = get_conf(grid_copy)
                path_copy.append("Right")
                if(cur_conf == tar_conf):
                    grid = grid_copy
                    moves = path_copy
                    return
                new_obj = params(grid_copy, empty_row, empty_col+1, obj.cost_so_far+1, path_copy)
                leaves.append(new_obj)
        # Left check
        if(empty_col != 0):
            grid_copy = deepcopy(grid)
            path_copy = deepcopy(path)
            swap_cells(grid_copy, empty_row, empty_col-1, empty_row, empty_col)
            if(is_dup_conf(grid_copy) == False):
                cur_conf = get_conf(grid_copy)
                path_copy.append("Left")
                if(cur_conf == tar_conf):
                    grid = grid_copy
                    moves = path_copy
                    return
                new_obj = params(grid_copy, empty_row, empty_col-1, obj.cost_so_far+1, path_copy)
                leaves.append(new_obj)

def handle_memory(leaves):
    global max_nodes
    if(len(leaves) > max_nodes):
        delete_max_cost_node(leaves)

def delete_max_cost_node(leaves):
    ind = 0
    max_cost = -1
    max_cost_ind = -1
    while(ind < len(leaves)):
        leaf = leaves[ind]
        cur_cost = leaf.total_cost
        if(cur_cost > max_cost):
            max_cost = cur_cost
            max_cost_ind = ind
        ind = ind+1
    del leaves[max_cost_ind]

def get_optimal_leaf(leaves):
    ind = 0
    min_cost = leaves[0].total_cost
    min_cost_ind = 0
    while(ind < len(leaves)):
        leaf = leaves[ind]
        cur_cost = leaf.total_cost
        if(cur_cost < min_cost):
            min_cost = cur_cost
            min_cost_ind = ind
        ind = ind+1
    tar_leaf = leaves[min_cost_ind]
    del leaves[min_cost_ind]
    return tar_leaf


def get_future_cost(obj_params):
    global rows
    obj_grid = obj_params.grid
    row = 0
    dist = 0
    while(row < rows):
        col = 0
        while(col < rows):
            cur_dist = manhattan_dist(obj_grid, row, col)
            dist = dist + cur_dist
            col = col+1
        row = row+1
    return dist

def manhattan_dist(grid, inp_row, inp_col):
    global tar_grid, rows
    inp_num = grid[inp_row][inp_col]
    row = 0
    while(row < rows):
        col = 0
        while(col < rows):
            cur_num = grid[row][col]
            if(inp_num == cur_num):
                return abs(row-inp_row)+abs(col-inp_col)
            col = col+1
        row = row+1

def is_dup_conf(grid):
    global configs
    prev_len = len(configs)
    cur_conf = get_conf(grid)
    configs.add(cur_conf)
    cur_len = len(configs)
    if(prev_len == cur_len):
        return True
    return False

def get_conf(g):
    s = ""
    cur_row = 0
    while(cur_row < len(g)):
        cur_col = 0
        while(cur_col < len(g[cur_row])):
            cur_num = g[cur_row][cur_col]
            s = s + str(cur_num) + ", "
            cur_col = cur_col+1
        cur_row = cur_row+1
    return s

def swap_cells(grid, row_1, col_1, row_2, col_2):
    temp = grid[row_1][col_1]
    grid[row_1][col_1] = grid[row_2][col_2]
    grid[row_2][col_2] = temp

def get_grid():
    f = open("../input.txt", "r")
    line = f.readline()
    n = int(line)
    grid = []
    while(True):
        line = f.readline()
        if(line is ""):
            break
        lst = line.split()
        lst = list(map(int, lst))
        grid.append(lst)
    f.close()
    return grid, n

def get_empty_cell():
    global grid
    row = 0
    while(row < rows):
        col = 0
        while(col < rows):
            num = grid[row][col]
            if(num == 0):
                return row, col
            col = col+1
        row = row+1

def print_set(s):
    for element in s:
        print(element)

def get_tar_conf():
    global rows, tar_grid
    num = 1
    row = 0
    tar_grid = []
    while(row < rows):
        col = 0
        new_row = []
        while(col < rows):
            new_row.append(num)
            num = num+1
            col = col+1
        tar_grid.append(new_row)
        row = row+1
    tar_grid[rows-1][rows-1] = 0
    return get_conf(tar_grid)

def is_solvable():
    lst = get_lst()
    ind = 0
    count = 0
    while(ind < len(lst)):
        num = lst[ind]
        inversions = get_inversions(lst, ind+1, len(lst)-1, num)
        count = count+inversions
        ind = ind+1
    if(count % 2 == 1):
        print("side note : InSolvable!")
        return
    print("Side note : Solvable!")

def get_inversions(lst, start, end, num):
    cur_ind = start
    count = 0
    while(cur_ind <= end):
        cur_num = lst[cur_ind]
        if(cur_num < num):
            count = count+1
        cur_ind = cur_ind+1
    return count

def get_lst():
    global grid, rows
    rows = len(grid)
    lst = []
    row = 0
    while(row < rows):
        col = 0
        while(col < rows):
            num = grid[row][col]
            if(num is not 0):
                lst.append(num)
            col = col+1
        row = row+1
    return lst 

global configs, grid, n, rows, tar_conf, empty_row, empty_col, iterations, max_nodes, max_deque_size, moves
max_nodes = 50
iterations=0
max_deque_size = -1
moves = []
configs = set()
grid, n = get_grid()
rows = int(sqrt(n+1))
tar_conf = get_tar_conf()
print("n : " + str(n))
print("raw grid : " + str(grid))
is_solvable()
print("A-Star in progress...")
a_star()
cur_conf = get_conf(grid)
print("cur_conf : " + cur_conf)
print("tar_conf : " + tar_conf)
if(cur_conf == tar_conf):
    print("Puzzle has been solved!")
else:
    print("Puzzle can't be solved!")
print("Post A-Star, Grid : " + str(grid))
end_time = time()
elapsed_time = end_time-start_time

print("Moves : " + str(moves))
print("Total Moves : " + str(len(moves)))
print(str(elapsed_time) + " seconds!")
print("iterations : " + str(iterations))
print("Max Deque Size : " + str(max_deque_size) + " nodes")
