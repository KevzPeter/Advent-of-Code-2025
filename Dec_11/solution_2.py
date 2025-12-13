'''
Advent of Code - Dec 11
Author: Kevin Peter
--- Part Two ---
Thanks in part to your analysis, the Elves have figured out a little bit about the issue. They now know that the problematic data path passes through both dac (a digital-to-analog converter) and fft (a device which performs a fast Fourier transform).

They're still not sure which specific path is the problem, and so they now need you to find every path from svr (the server rack) to out. However, the paths you find must all also visit both dac and fft (in any order).

For example:

svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
This new list of devices contains many paths from svr to out:

svr,aaa,fft,ccc,ddd,hub,fff,ggg,out
svr,aaa,fft,ccc,ddd,hub,fff,hhh,out
svr,aaa,fft,ccc,eee,dac,fff,ggg,out
svr,aaa,fft,ccc,eee,dac,fff,hhh,out
svr,bbb,tty,ccc,ddd,hub,fff,ggg,out
svr,bbb,tty,ccc,ddd,hub,fff,hhh,out
svr,bbb,tty,ccc,eee,dac,fff,ggg,out
svr,bbb,tty,ccc,eee,dac,fff,hhh,out
However, only 2 paths from svr to out visit both dac and fft.

Find all of the paths that lead from svr to out. How many of those paths visit both dac and fft?
'''
from functools import lru_cache
import sys
from os import path
import re
from collections import defaultdict

sample_input_file = path.join(path.dirname(__file__), 'sample_input_2.txt')
input_file = path.join(path.dirname(__file__), 'input.txt')

with open(input_file, 'r') as file:
    data = file.read().splitlines()


NEEDED = {"dac": 0, "fft": 1}  # node -> bit index


def bit_for(node: str) -> int:
    if node in NEEDED:
        return 1 << NEEDED[node]
    return 0


def parse(lines):
    g = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        left, right = line.split(":")
        u = left.strip()
        outs = right.strip().split()
        g[u] = outs
    # ensure all mentioned nodes exist in adjacency dict
    for u, outs in list(g.items()):
        for v in outs:
            g.setdefault(v, [])
    return g


def solve(lines):
    g = parse(lines)

    @lru_cache(None)
    def ways(u: str, mask: int) -> int:
        if u == "out":
            return 1 if mask == 0b11 else 0
        total = 0
        for v in g[u]:
            total += ways(v, mask | bit_for(v))
        return total

    start_mask = bit_for("svr")
    return ways("svr", start_mask)


print(solve(data))
