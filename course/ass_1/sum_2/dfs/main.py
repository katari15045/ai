from copy import deepcopy
from queue import LifoQueue
from time import time

start_time = time()

global rows
global colors
global configs
global stack, max_stack_size
global found
global iterations

class params:
    def __init__(self, grid, row, col):
        self.grid = grid
        self.row = row
        self.col = col

def bfs():
    global rows, colors, stack, found, iterations, max_stack_size
    grid = []
    init_grid(grid)
    new_grid = handle_cell(grid, 0, 0)
    if(found == True):
        return new_grid
    while(stack.qsize() != 0):
        iterations = iterations+1
        if(stack.qsize() > max_stack_size):
            max_stack_size = stack.qsize()
        obj = stack.get()
        row = obj.row
        col = obj.col
        grid = obj.grid
        new_grid = handle_cell(grid, row, col)
        if(found == True):
            return new_grid
    print("No Solution Exists")
    return grid
    
def handle_cell(grid, row, col):
    global stack, rows, colors, found
    count = 1
    while(count <= colors):
        new_grid = deepcopy(grid)
        new_grid[row][col] = count
        if(is_valid(new_grid) == True and is_duplicate(new_grid) == False):
            if(col != (rows-1)):
                col = col+1
            elif(row != (rows-1)):
                row = row+1
                col = 0
            elif(no_zero(new_grid) == True):
                found = True
                return new_grid
            obj = params(new_grid, row, col)
            stack.put(obj)
        count = count+1

def no_zero(grid):
    global rows
    row = 0
    while(row < rows):
        col = 0
        while(col < rows):
            num = grid[row][col]
            if(num == 0):
                return False
            col = col+1
        row = row+1
    return True

def is_duplicate(grid):
        global configs
        cur_conf = get_config(grid)
        prev_len = len(configs)
        configs.add(cur_conf)
        cur_len = len(configs)
        if(prev_len == cur_len):
            return True
        return False

def get_config(grid):
    global rows
    row = 0
    s = ""
    while(row < rows):
        col = 0
        while(col < rows):
            cur_str = str(grid[row][col])
            s = s + cur_str + ","
            col = col+1
        row = row+1
    return s

def is_valid(grid):
    global rows
    row = 0
    while(row < rows):
        col = 0
        while(col < rows):
            cur_color = grid[row][col]
            if(col != 0):
                left_color = grid[row][col-1]
                if(cur_color == left_color and cur_color != 0):
                    return False
            if(row != 0):
                top_color = grid[row-1][col]
                if(cur_color == top_color and cur_color != 0):
                    return False
            col = col+1
        row = row+1
    return True

def init_grid(grid):
    row = 0
    while(row < rows):
        col = 0
        new_row = []
        while(col < rows):
            new_row.append(0)
            col = col+1
        grid.append(new_row)
        row = row+1

global rows, colors, configs, stack, iterations, max_stack_size
rows = 3
colors = 4
iterations = 0
max_stack_size = -1
configs = set()
stack = LifoQueue()
found = False
g = bfs()
print(g)
end_time = time()
elapsed_time = end_time-start_time

print(str(elapsed_time) + " seconds!")
print(str(iterations) + " iterations")
print("Max Stack Size : " + str(max_stack_size) + " nodes")
