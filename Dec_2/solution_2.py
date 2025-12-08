from os import path

sample_input_file = path.join(path.dirname(__file__), 'sample_input.txt')
input_file = path.join(path.dirname(__file__), 'input.txt')

with open(input_file, 'r') as file:
    data = file.read().split(',')

final_ans = 0


def check_repeated_substring_pattern(s: str) -> bool:
    n = len(s)
    for i in range(n // 2, 0, -1):
        if n % i == 0:
            if s[:i] * (n // i) == s:
                return True
    return False


for interval in data:
    start, end = map(int, interval.split('-'))
    for i in range(start, end + 1):
        str_i = str(i)
        if (check_repeated_substring_pattern(str_i)):
            final_ans += int(str_i)

print(final_ans)
