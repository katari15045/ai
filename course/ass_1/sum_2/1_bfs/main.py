from queue import Queue
from copy import deepcopy
from time import time

start_time = time()

global n, iters, max_q_size

def read_inp(file_name):
    global n, iters
    book = open(file_name)
    line = book.readline()
    n = int(line)
    grid = []
    while(True):
        line = book.readline()
        if(line == ""):
            break
        lst = line.split()
        lst = list(map(int, lst))
        grid.append(lst)
    book.close()
    return grid

def is_grid_valid(grid):
    global n
    row = 0
    while(row < n):
        col = 0
        while(col < n):
            cur_num = grid[row][col]
            if(col != 0 and cur_num != 0):
                left_num = grid[row][col-1]
                if(cur_num == left_num):
                    return False
            if(row != 0 and cur_num != 0):
                top_num = grid[row-1][col]
                if(top_num == cur_num):
                    return False
            col = col+1
        row = row+1
    return True

def get_empty_grid():
    global n
    row = 0
    grid = []
    while(row < n):
        col = 0
        new_row = []
        while(col < n):
            new_row.append(0)
            col = col+1
        grid.append(new_row)
        row = row+1
    return grid

def get_max(grid):
    global n
    row = 0
    max_ = -1
    while(row < n):
        cur_row = grid[row]
        row_max = max(cur_row)
        max_ = max(row_max, max_)
        row = row+1
    return max_

def init_freq_lst(length):
    count = 0
    lst = []
    while(count < length):
        lst.append(0)
        count = count+1
    return lst


def get_freq_lst(grid):
    global n
    max_ = get_max(grid)
    freq_lst = init_freq_lst(max_)
    row = 0
    while(row < n):
        col = 0
        while(col < n):
            cur_num = grid[row][col]
            freq_lst[cur_num-1] = freq_lst[cur_num-1]+1
            col = col+1
        row = row+1
    return freq_lst


class params():
    def __init__(self, grid, row, col, freq_lst):
        self.grid = grid
        self.row = row
        self.col = col
        self.freq_lst = freq_lst

def has_zeros(grid):
    global n
    row = 0
    while(row < n):
        col = 0
        while(col < n):
            cur_num = grid[row][col]
            if(cur_num == 0):
                return True
            col = col+1
        row = row+1
    return False

def bfs(freq_lst):
    global n, iters, max_q_size
    iters = 0
    max_q_size = -1
    q = Queue()
    grid = get_empty_grid()
    obj = params(grid, 0, 0, freq_lst)
    q.put(obj)
    while(q.qsize() != 0):
        max_q_size = max(q.qsize(), max_q_size)
        obj = q.get()
        grid = obj.grid
        row = obj.row
        col = obj.col
        freq_lst = obj.freq_lst
        freq_ind = 0
        iters = iters+1
        if(row < n):
            while(freq_ind < len(freq_lst)):
                freq_num = freq_lst[freq_ind]
                if(freq_num != 0):
                    freq_lst_cpy = deepcopy(freq_lst)
                    grid_cpy = deepcopy(grid)
                    freq_lst_cpy[freq_ind] = freq_lst_cpy[freq_ind]-1
                    grid_cpy[row][col] = freq_ind+1
                    if(is_grid_valid(grid_cpy) == True):
                        if(row == (n-1) and col == (n-1) and has_zeros(grid_cpy) == False):
                            return grid_cpy
                        if(col == (n-1)):
                            new_col = 0
                            new_row = row+1
                        else:
                            new_col = col+1
                            new_row = row
                        obj = params(grid_cpy, new_row, new_col, freq_lst_cpy)
                        q.put(obj)
                        max_q_size = max(q.qsize(), max_q_size)
                freq_ind = freq_ind+1
    return []

def main():
    global iters, max_q_size
    grid = read_inp("../input.txt")
    print("Raw Grid : " + str(grid))
    if(is_grid_valid(grid) == True):
        print("Given grid is a valid grid!")
        return
    freq_lst = get_freq_lst(grid)
    print("freq_lst : " + str(freq_lst))
    grid = bfs(freq_lst)
    if(len(grid) == 0):
        print("Solution doesn't exist!")
    else:
        print("Solution : " + str(grid))
    print("Max Queue size : " + str(max_q_size))
    print("iterations : " + str(iters))

main()
end_time = time()
elapsed_time = end_time - start_time
print(str(elapsed_time) + " seconds!")
