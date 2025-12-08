from os import path

input_file = path.join(path.dirname(__file__), 'input.txt')
sample_input_file = path.join(path.dirname(__file__), 'sample_input.txt')

with open(input_file, 'r') as file:
    data = file.read().strip().split('\n')

total_joltage = 0
num_batteries = 12

for bank in data:
    result = []
    start_pos = 0

    for _ in range(num_batteries):
        remaining_to_select = num_batteries - len(result)
        # Find the largest digit from start_pos to the last valid position
        # (must leave enough digits for remaining selections)
        end_pos = len(bank) - remaining_to_select + 1

        largest_digit = max(int(bank[i]) for i in range(start_pos, end_pos))
        largest_pos = bank.find(str(largest_digit), start_pos, end_pos)

        result.append(str(largest_digit))
        start_pos = largest_pos + 1

    joltage = int(''.join(result))
    total_joltage += joltage

print(f"Total joltage: {total_joltage}")
