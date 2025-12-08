from os import path

sample_input_file = path.join(path.dirname(__file__), 'sample_input.txt')
input_file = path.join(path.dirname(__file__), 'input.txt')

with open(input_file, 'r') as file:
    data = file.read().split(',')

final_ans = 0

for interval in data:
    start, end = map(int, interval.split('-'))
    for i in range(start, end + 1):
        str_i = str(i)
        if ((len(str_i) % 2 == 0) and str_i[:len(str_i)//2] == str_i[len(str_i)//2:]):
            final_ans += int(str_i)

print(final_ans)
