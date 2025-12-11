'''
--- Part Two ---
The Elves were right; they definitely don't have enough extension cables. You'll need to keep connecting junction boxes together until they're all in one large circuit.

Continuing the above example, the first connection which causes all of the junction boxes to form a single circuit is between the junction boxes at 216,146,977 and 117,168,530. The Elves need to know how far those junction boxes are from the wall so they can pick the right extension cable; multiplying the X coordinates of those two junction boxes (216 and 117) produces 25272.

Continue connecting the closest unconnected pairs of junction boxes together until they're all in the same circuit. What do you get if you multiply together the X coordinates of the last two junction boxes you need to connect?
'''
import heapq
from os import path

sample_input_file = path.join(path.dirname(__file__), 'sample_input.txt')
input_file = path.join(path.dirname(__file__), 'input.txt')

with open(input_file, 'r') as file:
    data = [list(map(int, line.split(','))) for line in file.read().splitlines()]


def compute3d_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2) + ((p1[2] - p2[2]) ** 2)


max_heap = []

for i in range(len(data)):
    x, y, z = data[i]
    for j in range(i+1, len(data)):
        x2, y2, z2 = data[j]
        dist = compute3d_distance((x, y, z), (x2, y2, z2))
        heapq.heappush(max_heap, (dist, i, j))

parent = [i for i in range(len(data))]
rank = [1] * len(data)


def find(u):
    if parent[u] != u:
        parent[u] = find(parent[u])
    return parent[u]


def union(u, v):
    pu, pv = find(u), find(v)
    if pu != pv:
        if rank[pu] > rank[pv]:
            parent[pv] = pu
        elif rank[pv] > rank[pu]:
            parent[pu] = pv
        else:
            parent[pv] = pu
            rank[pu] += 1


while max_heap:
    dist, u, v = heapq.heappop(max_heap)
    union(u, v)
    unique_parents_after_union = len(set(find(i) for i in range(len(data))))
    if unique_parents_after_union == 1:
        x1, y1, z1 = data[u]
        x2, y2, z2 = data[v]
        print(f"Last connection is between junction boxes at ({x1},{y1},{z1}) and ({x2},{y2},{z2})")
        print(f"Product of their X coordinates: {x1 * x2}")
        break
