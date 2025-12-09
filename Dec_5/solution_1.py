from os import path

sample_input_file = path.join(path.dirname(__file__), 'sample_input.txt')
input_file = path.join(path.dirname(__file__), 'input.txt')

with open(input_file, 'r') as file:
    data = file.read().split('\n\n')
    fresh_ranges, ingredient_ids = map(lambda x: x.split('\n'), data)

fresh_ranges_tuples = [tuple(map(int, r.split('-'))) for r in fresh_ranges]
fresh_ranges_sorted = sorted(fresh_ranges_tuples, key=lambda x: (x[0], x[1]))

total_fresh_ingredients = 0
for ingredient_id in ingredient_ids:
    ingredient_id = int(ingredient_id)
    for fr in fresh_ranges_sorted:
        if fr[0] <= ingredient_id <= fr[1]:
            total_fresh_ingredients += 1
            break

print(total_fresh_ingredients)
