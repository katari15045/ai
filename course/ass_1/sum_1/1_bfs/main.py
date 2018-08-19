from math import sqrt
from queue import Queue
from time import time
from copy import deepcopy

start_time = time()
global grid
global n, rows
global tar_conf
global iterations
global max_q_size
global moves

class params():
    def __init__(self, grid, empty_row, empty_col, path):
        self.grid = grid
        self.empty_row = empty_row
        self.empty_col = empty_col
        self.path = path

def bfs():
    global n, grid, configs, rows, configs, iterations, max_q_size, moves
    queue = Queue()
    rows = int(sqrt(n+1))
    empty_row, empty_col = get_empty_cell()
    obj = params(deepcopy(grid), empty_row, empty_col, [])
    queue.put(obj)
    while(queue.qsize() is not 0):
        iterations = iterations+1
        if(queue.qsize() > max_q_size):
            max_q_size = queue.qsize()
        obj = queue.get()
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
                if(cur_conf == tar_conf):
                    grid = grid_copy
                    moves = path
                    return
                path_copy.append("Down")
                obj = params(grid_copy, empty_row+1, empty_col, path_copy)
                queue.put(obj)
        # Top Check
        if(empty_row != 0):
            grid_copy = deepcopy(grid)
            path_copy = deepcopy(path)
            swap_cells(grid_copy, empty_row-1, empty_col, empty_row, empty_col)
            if(is_dup_conf(grid_copy) == False):
                cur_conf = get_conf(grid_copy)
                if(cur_conf == tar_conf):
                    grid = grid_copy
                    moves = path
                    return
                path_copy.append("Up")
                obj = params(grid_copy, empty_row-1, empty_col, path_copy)
                queue.put(obj)
        # Right Check
        if(empty_col != (rows-1)):
            grid_copy = deepcopy(grid)
            path_copy = deepcopy(path)
            swap_cells(grid_copy, empty_row, empty_col+1, empty_row, empty_col)
            if(is_dup_conf(grid_copy) == False):
                cur_conf = get_conf(grid_copy)
                if(cur_conf == tar_conf):
                    grid = grid_copy
                    moves = path
                    return
                path_copy.append("Right")
                obj = params(grid_copy, empty_row, empty_col+1, path_copy)
                queue.put(obj)
        # Left check
        if(empty_col != 0):
            grid_copy = deepcopy(grid)
            path_copy = deepcopy(path)
            swap_cells(grid_copy, empty_row, empty_col-1, empty_row, empty_col)
            if(is_dup_conf(grid_copy) == False):
                cur_conf = get_conf(grid_copy)
                if(cur_conf == tar_conf):
                    grid = grid_copy
                    moves = path
                    return
                path_copy.append("Left")
                obj = params(grid_copy, empty_row, empty_col-1, path_copy)
                queue.put(obj)
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
    global rows
    num = 1
    row = 0
    grid = []
    while(row < rows):
        col = 0
        new_row = []
        while(col < rows):
            new_row.append(num)
            num = num+1
            col = col+1
        grid.append(new_row)
        row = row+1
    grid[rows-1][rows-1] = 0
    return get_conf(grid)

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

global configs, grid, n, rows, tar_conf, empty_row, empty_col, iterations, max_q_size, moves
iterations=0
max_q_size = -1
moves = []
configs = set()
grid, n = get_grid()
rows = int(sqrt(n+1))
tar_conf = get_tar_conf()
print("n : " + str(n))
print("raw grid : " + str(grid))
is_solvable()
print("BFS in progress...")
bfs()
cur_conf = get_conf(grid)
print("cur_conf : " + cur_conf)
print("tar_conf : " + tar_conf)
if(cur_conf == tar_conf):
    print("Puzzle has been solved!")
else:
    print("Puzzle can't be solved!")
print("Post BFS, Grid : " + str(grid))
end_time = time()
elapsed_time = end_time-start_time

print("Moves : " + str(moves))
print(str(elapsed_time) + " seconds!")
print("iterations : " + str(iterations))
print("Max Queue Size : " + str(max_q_size) + " Nodes")

