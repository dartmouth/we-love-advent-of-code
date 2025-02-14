#!/usr/bin/env python3

import sys
import re
from sympy import symbols, Eq, solve

with open("src/day-13/input.txt", "r") as f:
    chunks = f.read().split("\n\n")

part1 = 0
part2 = 0
for c in chunks:
    c = c.replace("+", "=")
    xs = list(map(int, re.findall(r"X=(\d+)", c)))
    ys = list(map(int, re.findall(r"Y=(\d+)", c)))

    n, m = symbols("n m", integer=True)

    eq1 = Eq(xs[0] * n + xs[1] * m, xs[2])
    eq2 = Eq(ys[0] * n + ys[1] * m, ys[2])
    solution = solve((eq1, eq2), (n, m))
    if solution:
        part1 += solution[n] * 3 + solution[m]

    eq1 = Eq(xs[0] * n + xs[1] * m, xs[2] + 10000000000000)
    eq2 = Eq(ys[0] * n + ys[1] * m, ys[2] + 10000000000000)
    solution = solve((eq1, eq2), (n, m))
    if solution:
        part2 += solution[n] * 3 + solution[m]

print(f"Solution 1: {part1}")
print(f"Solution 2: {part2}")
