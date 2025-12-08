from os import path

sample_input_file = path.join(path.dirname(__file__), 'sample_input.txt')
input_file = path.join(path.dirname(__file__), 'input.txt')

with open(input_file, 'r') as file:
    data = file.read().split('\n')

total_joltage = 0

for bank in data:
    max_digit_suffix = [0 for _ in range(len(bank))]
    digit_map = {}
    # O(n)
    for i in range(len(bank)-1, -1, -1):
        digit = int(bank[i])
        digit_map[digit] = i
        max_digit_suffix[i] = max(digit, max_digit_suffix[i+1] if i+1 < len(bank) else digit)
    # O(1)
    for digit in range(9, 0, -1):
        if digit in digit_map and digit_map[digit] < len(bank) - 1:
            max_joltage_bank = digit * 10 + max_digit_suffix[digit_map[digit] + 1]
            break

    total_joltage += max_joltage_bank

print(f"Total joltage: {total_joltage}")
