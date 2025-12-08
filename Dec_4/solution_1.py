from os import path

sample_input_file = path.join(path.dirname(__file__), 'sample_input.txt')
input_file = path.join(path.dirname(__file__), 'input.txt')

with open(input_file, 'r') as file:
    data = file.read().split('\n')


def create_grid(data):
    grid = []
    for line in data:
        grid.append([x for x in line])
    return grid


grid = create_grid(data)

m = len(grid)
n = len(grid[0])

dirs = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]

total_rolls = 0


def is_valid(i, j):
    return 0 <= i < m and 0 <= j < n


for i in range(m):
    for j in range(n):
        if (grid[i][j] != '@'):
            continue
        adjacent_rolls = 0
        for dir in dirs:
            x, y = i + dir[0], j + dir[1]
            if is_valid(x, y) and grid[x][y] == '@':
                adjacent_rolls += 1
        if (adjacent_rolls < 4):
            total_rolls += 1

print(total_rolls)
