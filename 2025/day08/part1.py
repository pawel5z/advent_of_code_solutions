# python3 10 < example.input
# python3 1000 < puzzle.input

import sys
import math
from itertools import combinations
from operator import mul
from functools import reduce


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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: <python> {sys.argv[0]} pair_count")
        sys.exit(0)

    TARGET_CONN_CNT = int(sys.argv[1])

    boxes: list[tuple[int, int, int]] = []
    for line in sys.stdin.readlines():
        boxes.append(tuple(map(int, line.strip().split(","))))

    closest_pairs = sorted(
        combinations(range(len(boxes)), r=2),
        key=lambda p: square_dist(boxes[p[0]], boxes[p[1]]),
    )
    # print(closest_pairs)

    box_to_set = {b: {b} for b in range(len(boxes))}
    conn_cnt = 0
    for b1, b2 in closest_pairs:
        if conn_cnt == TARGET_CONN_CNT:
            break
        if box_to_set[b1] is box_to_set[b2]:
            continue
        box_to_set[b1].update(box_to_set[b2])
        for k in box_to_set:
            if box_to_set[k] is box_to_set[b2]:
                box_to_set[k] = box_to_set[b1]
        conn_cnt += 1

        # print(f"--- {b1, b2} ---")
        # for k, v in box_to_set.items():
        #     print(v)

    # for k, v in box_to_set.items():
    #     print(v)

    largest_sizes = []
    for _ in range(3):
        b = max(box_to_set, key=lambda b1: len(box_to_set[b1]))
        largest_sizes.append(len(box_to_set[b]))
        b_set = box_to_set[b]
        to_remove = []
        for k, v in box_to_set.items():
            if v is b_set:
                to_remove.append(k)
        for k in to_remove:
            box_to_set.pop(k)

    print(reduce(mul, largest_sizes, 1))
