from __future__ import annotations
from collections import deque
from os import path
from typing import List, Tuple, Dict

Point = Tuple[int, int]

input_file = path.join(path.dirname(__file__), "input.txt")


def parse_points(text: str) -> List[Point]:
    pts = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        x, y = line.split(",")
        pts.append((int(x), int(y)))
    return pts


def compress_coords(loop: List[Point]) -> Tuple[List[int], List[int]]:
    # Model each tile (x,y) as the unit square [x, x+1) x [y, y+1)
    xs = set()
    ys = set()
    n = len(loop)

    for i in range(n):
        x1, y1 = loop[i]
        x2, y2 = loop[(i + 1) % n]

        # add edges for endpoints
        xs.add(x1)
        xs.add(x1 + 1)
        ys.add(y1)
        ys.add(y1 + 1)

        xs.add(x2)
        xs.add(x2 + 1)
        ys.add(y2)
        ys.add(y2 + 1)

        # add edges for the whole segment span
        if x1 == x2:
            lo, hi = sorted((y1, y2))
            ys.add(lo)
            ys.add(hi + 1)
            ys.add(lo + 1)
            ys.add(hi)  # helps keep adjacency correct
        elif y1 == y2:
            lo, hi = sorted((x1, x2))
            xs.add(lo)
            xs.add(hi + 1)
            xs.add(lo + 1)
            xs.add(hi)
        else:
            raise ValueError("Consecutive points must share row or column")

    # Add a padding frame so outside flood-fill has room
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    xs.add(minx - 1)
    xs.add(maxx + 1)
    ys.add(miny - 1)
    ys.add(maxy + 1)

    xs = sorted(xs)
    ys = sorted(ys)
    return xs, ys


def build_index_map(vals: List[int]) -> Dict[int, int]:
    return {v: i for i, v in enumerate(vals)}


def mark_boundary_blocks(loop: List[Point], xs: List[int], ys: List[int]) -> List[List[bool]]:
    xi = build_index_map(xs)
    yi = build_index_map(ys)

    W = len(xs) - 1  # blocks
    H = len(ys) - 1
    blocked = [[False] * W for _ in range(H)]

    def mark_rect(xa: int, xb: int, ya: int, yb: int):
        # mark blocks that intersect [xa, xb) x [ya, yb)
        ia0 = xi[xa]
        ia1 = xi[xb]
        ib0 = yi[ya]
        ib1 = yi[yb]
        for j in range(ib0, ib1):
            row = blocked[j]
            for i in range(ia0, ia1):
                row[i] = True

    n = len(loop)
    for k in range(n):
        (x1, y1) = loop[k]
        (x2, y2) = loop[(k + 1) % n]
        if x1 == x2:
            lo, hi = sorted((y1, y2))
            # boundary tiles cover x in [x1, x1+1) and y in [lo, hi+1)
            mark_rect(x1, x1 + 1, lo, hi + 1)
        else:
            lo, hi = sorted((x1, x2))
            # boundary tiles cover x in [lo, hi+1) and y in [y1, y1+1)
            mark_rect(lo, hi + 1, y1, y1 + 1)

    return blocked


def flood_fill_outside(blocked: List[List[bool]]) -> List[List[bool]]:
    H = len(blocked)
    W = len(blocked[0])
    outside = [[False] * W for _ in range(H)]
    q = deque()

    # start from all border blocks that are not blocked
    for x in range(W):
        if not blocked[0][x]:
            outside[0][x] = True
            q.append((0, x))
        if not blocked[H - 1][x]:
            outside[H - 1][x] = True
            q.append((H - 1, x))
    for y in range(H):
        if not blocked[y][0]:
            outside[y][0] = True
            q.append((y, 0))
        if not blocked[y][W - 1]:
            outside[y][W - 1] = True
            q.append((y, W - 1))

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while q:
        y, x = q.popleft()
        for dy, dx in dirs:
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < W and not outside[ny][nx] and not blocked[ny][nx]:
                outside[ny][nx] = True
                q.append((ny, nx))

    return outside


def build_allowed_prefix(xs: List[int], ys: List[int], blocked, outside):
    # allowed blocks are boundary (blocked=True) plus interior (not outside and not blocked)
    H = len(blocked)
    W = len(blocked[0])

    # prefix sum over tile-count area, not just block count
    ps = [[0] * (W + 1) for _ in range(H + 1)]
    for j in range(H):
        height = ys[j + 1] - ys[j]
        row_sum = 0
        for i in range(W):
            width = xs[i + 1] - xs[i]
            allowed = blocked[j][i] or (not blocked[j][i] and not outside[j][i])
            area = width * height if allowed else 0
            row_sum += area
            ps[j + 1][i + 1] = ps[j][i + 1] + row_sum
    return ps


def rect_sum(ps, x0, x1, y0, y1):
    # sum over [y0, y1) x [x0, x1) in compressed block indices
    return ps[y1][x1] - ps[y0][x1] - ps[y1][x0] + ps[y0][x0]


def solve_part2(loop: List[Point]) -> int:
    xs, ys = compress_coords(loop)
    xi = build_index_map(xs)
    yi = build_index_map(ys)

    blocked = mark_boundary_blocks(loop, xs, ys)
    outside = flood_fill_outside(blocked)
    ps = build_allowed_prefix(xs, ys, blocked, outside)

    red = loop[:]  # red corners are exactly the listed points
    n = len(red)

    best = 0
    # Area is inclusive: (abs(dx)+1)*(abs(dy)+1)
    for a in range(n):
        x1, y1 = red[a]
        for b in range(a + 1, n):
            x2, y2 = red[b]
            if x1 == x2 or y1 == y2:
                continue

            rx0, rx1 = (x1, x2) if x1 < x2 else (x2, x1)
            ry0, ry1 = (y1, y2) if y1 < y2 else (y2, y1)

            area = (rx1 - rx0 + 1) * (ry1 - ry0 + 1)
            if area <= best:
                continue

            # rectangle tiles correspond to [rx0, rx1+1) x [ry0, ry1+1) in tile-square coordinates
            # map to compressed indices
            cx0 = xi[rx0]
            cx1 = xi[rx1 + 1]
            cy0 = yi[ry0]
            cy1 = yi[ry1 + 1]

            allowed_area = rect_sum(ps, cx0, cx1, cy0, cy1)
            if allowed_area == area:
                best = area

    return best


if __name__ == "__main__":
    with open(input_file, "r", encoding="utf-8") as f:
        loop = parse_points(f.read())

    print(solve_part2(loop))
