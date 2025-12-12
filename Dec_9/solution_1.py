from os import path

sample_input_file = path.join(path.dirname(__file__), 'sample_input.txt')
input_file = path.join(path.dirname(__file__), 'input.txt')

with open(input_file, 'r') as file:
    data = [list(map(int, line.split(','))) for line in file.read().splitlines()]

largest_rectangle_area = 0

for i in range(len(data)):
    x, y = data[i]
    for j in range(len(data)):
        if i != j:
            x2, y2 = data[j]
            area = abs(x - x2 + 1) * abs(y - y2 + 1)
            largest_rectangle_area = max(largest_rectangle_area, area)

print(largest_rectangle_area)
