# python3 10 < example.input
# python3 1000 < puzzle.input

import sys
import math
from itertools import combinations
from operator import mul
from functools import reduce
from typing import defaultdict


def square_dist(b1, b2):
    return sum(
        map(
            lambda x: x*x,
            map(
                lambda x: x[0] - x[1],
                zip(b1, b2)
            )
        )
    )


def find(e: int, parents: list[int]) -> int:
    if e != parents[e]:
        parents[e] = find(parents[e], parents)
    return parents[e]


def print_sets(parents: list[int]):
    n = len(parents)
    sets = defaultdict(list)
    for i in range(n):
        sets[find(i, parents)].append(i)
    for _, v in sets.items():
        if len(v) > 1:
            print(v)


if __name__ == "__main__":
    n = 0
    boxes: list[tuple[int, int, int]] = []
    for line in sys.stdin.readlines():
        boxes.append(tuple(map(int, line.strip().split(","))))
        n += 1

    closest_pairs = sorted(
        combinations(range(n), r=2),
        key=lambda p: square_dist(boxes[p[0]], boxes[p[1]]),
    )

    parents = list(range(n))
    for b1, b2 in closest_pairs:
        if find(b1, parents) == find(b2, parents):
            continue
        parents[find(b2, parents)] = find(b1, parents)
        maybe_global_root = find(0, parents)
        if all(map(lambda e: find(e, parents) == maybe_global_root, parents)):
            print(boxes[b1][0] * boxes[b2][0])
