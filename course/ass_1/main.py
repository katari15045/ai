from math import sqrt
from queue import LifoQueue
from time import time

start_time = time()

class dfs_params:
    def __init__(self, grid, n, empty_row, empty_col, configs, tar_conf):
        self.grid = grid
        self.n = n
        self.empty_row = empty_row
        self.empty_col = empty_col
        self.configs = configs
        self.tar_conf = tar_conf

def dfs(grid, n, empty_row, empty_col, configs, tar_conf):
    stack = LifoQueue()
    rows = int(sqrt(n+1))
    obj = dfs_params(grid, n, empty_row, empty_col, configs, tar_conf)
    stack.put(obj)
    while(stack.qsize() is not 0):
        obj = stack.get()
        grid = obj.grid
        n = obj.n
        empty_row = obj.empty_row
        empty_col = obj.empty_col
        configs = obj.configs
        tar_conf = obj.tar_conf
        # Bottom Check
        if(empty_row != (rows-1)):
            swap_cells(grid, empty_row+1, empty_col, empty_row, empty_col)
            if(is_dup_conf(grid, configs) == True):
                swap_cells(grid, empty_row+1, empty_col, empty_row, empty_col)
            else:
                cur_conf = get_conf(grid)
                if(cur_conf == tar_conf):
                    print("tar_conf")
                    return
                empty_row = empty_row+1
                obj = dfs_params(grid, n, empty_row, empty_col, configs, tar_conf)
                stack.put(obj)
        # Top Check
        if(empty_row != 0):
            swap_cells(grid, empty_row-1, empty_col, empty_row, empty_col)
            if(is_dup_conf(grid, configs) == True):
                swap_cells(grid, empty_row-1, empty_col, empty_row, empty_col)
            else:
                cur_conf = get_conf(grid)
                if(cur_conf == tar_conf):
                    print("tar_conf")
                    return
                empty_row = empty_row-1
                obj = dfs_params(grid, n, empty_row, empty_col, configs, tar_conf)
                stack.put(obj)
        # Right Check
        if(empty_col != (rows-1)):
            swap_cells(grid, empty_row, empty_col+1, empty_row, empty_col)
            if(is_dup_conf(grid, configs) == True):
                swap_cells(grid, empty_row, empty_col+1, empty_row, empty_col)
            else:
                cur_conf = get_conf(grid)
                if(cur_conf == tar_conf):
                    print("tar_conf")
                    return
                empty_col = empty_col + 1
                obj = dfs_params(grid, n, empty_row, empty_col, configs, tar_conf)
                stack.put(obj)
        # Left check
        if(empty_col != 0):
            swap_cells(grid, empty_row, empty_col-1, empty_row, empty_col)
            if(is_dup_conf(grid, configs) == True):
                swap_cells(grid, empty_row, empty_col-1, empty_row, empty_col)
            else:
                cur_conf = get_conf(grid)
                if(cur_conf == tar_conf):
                    print("tar_conf")
                    return
                empty_col = empty_col-1
                obj = dfs_params(grid, n, empty_row, empty_col, configs, tar_conf)
                stack.put(obj)
def is_dup_conf(grid, configs):
    prev_len = len(configs)
    cur_conf = get_conf(grid)
    configs.add(cur_conf)
    cur_len = len(configs)
    if(prev_len == cur_len):
        return True
    return False

def get_conf(grid):
    s = ""
    cur_row = 0
    while(cur_row < len(grid)):
        cur_col = 0
        while(cur_col < len(grid[cur_row])):
            cur_num = grid[cur_row][cur_col]
            s = s + str(cur_num) + ", "
            cur_col = cur_col+1
        cur_row = cur_row+1
    return s

def swap_cells(grid, row_1, col_1, row_2, col_2):
    temp = grid[row_1][col_1]
    grid[row_1][col_1] = grid[row_2][col_2]
    grid[row_2][col_2] = temp

def get_grid():
    f = open("input.txt", "r")
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

def get_empty_cell(grid, rows):
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

def get_tar_conf(rows):
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

configs = set()
grid, n = get_grid()
rows = int(sqrt(n+1))
tar_conf = get_tar_conf(rows)
empty_row, empty_col = get_empty_cell(grid, rows)
print("n : " + str(n))
print("raw grid : " + str(grid))
print("empty cell : " + str(empty_row) + ", " + str(empty_col))
print("tar Conf : " + str(tar_conf))
dfs(grid, n, empty_row, empty_col, configs, tar_conf)
print("grid post DFS : " + str(grid))

end_time = time()
elapsed_time = end_time-start_time
print(str(elapsed_time) + " seconds!")
