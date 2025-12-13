import re
from os import path

sample_input_file = path.join(path.dirname(__file__), 'sample_input.txt')
input_file = path.join(path.dirname(__file__), 'input.txt')

with open(input_file, 'r') as file:
    input = file.read()
    *raw_shapes, raw_regions = input.split("\n\n")

SHAPE_WIDTH = SHAPE_HEIGHT = 3

# Get the number of tiles in each shape
shape_num_tiles: list[int] = []
for raw_shape in raw_shapes:
    _, *grid = raw_shape.splitlines()
    assert len(grid) == SHAPE_HEIGHT
    assert all(len(row) == SHAPE_WIDTH for row in grid)
    shape_num_tiles.append(sum(ch == "#" for row in grid for ch in row))

total = 0
for raw_region in raw_regions.splitlines():
    width, height, *shape_quantities = (map(int, re.findall(r"\d+", raw_region)))
    # If this amount of presents definitely fits, add to tally
    max_presents_lower_bound = ((width // SHAPE_WIDTH) * (height // SHAPE_HEIGHT))
    num_presents = sum(shape_quantities)
    if num_presents <= max_presents_lower_bound:
        total += 1
        continue
    # Skip if lower bound of tile count won't fit in the region
    num_tiles_lower_bound = sum(tiles * quantity for tiles, quantity in zip(shape_num_tiles, shape_quantities))
    region_num_tiles = width * height
    if num_tiles_lower_bound > region_num_tiles:
        continue


print(total)
