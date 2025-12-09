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
    if len(sys.argv) < 2:
        print(f"Usage: <python> {sys.argv[0]} pair_count")
        sys.exit(0)

    TARGET_CONN_CNT = int(sys.argv[1])

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
    conn_cnt = 0
    for b1, b2 in closest_pairs:
        if conn_cnt == TARGET_CONN_CNT:
            break
        conn_cnt += 1
        # print(f"--- {b1, b2} ---")
        if find(b1, parents) == find(b2, parents):
            continue
        parents[find(b2, parents)] = find(b1, parents)
        # print_sets(parents)

    # for i in range(n):
    #     print(f"{i}: {find(i, parents)}")

    sizes = defaultdict(int)
    for e in range(n):
        sizes[find(e, parents)] += 1

    # for k, v in sizes.items():
    #     print(k, v)

    largest_sizes = []
    for _ in range(3):
        max_size_representative = max(sizes.keys(), key=lambda k: sizes[k])
        largest_sizes.append(sizes[max_size_representative])
        sizes.pop(max_size_representative)

    print(reduce(mul, largest_sizes, 1))
