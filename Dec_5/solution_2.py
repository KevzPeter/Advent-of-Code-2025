from os import path

sample_input_file = path.join(path.dirname(__file__), 'sample_input.txt')
input_file = path.join(path.dirname(__file__), 'input.txt')

with open(input_file, 'r') as file:
    data = file.read().split('\n\n')
    fresh_ranges, ingredient_ids = map(lambda x: x.split('\n'), data)

fresh_ranges_tuples = [tuple(map(int, r.split('-'))) for r in fresh_ranges]
fresh_ranges_sorted = sorted(fresh_ranges_tuples, key=lambda x: (x[0], x[1]))


def merge_intervals(intervals):
    merged = []
    for current in intervals:
        if not merged or merged[-1][1] < current[0]:
            merged.append(current)
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], current[1]))
    return merged


merged_fresh_ranges = merge_intervals(fresh_ranges_sorted)

total_fresh_ingredients = 0
for fresh_ranges in merged_fresh_ranges:
    total_fresh_ingredients += fresh_ranges[1] - fresh_ranges[0] + 1

print(total_fresh_ingredients)
