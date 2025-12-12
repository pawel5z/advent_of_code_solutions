import sys
from itertools import combinations


def area(t1, t2):
    return (abs(t1[0]-t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)


if __name__ == "__main__":
    tiles = []
    for line in sys.stdin.readlines():
        tiles.append(tuple(map(int, line.strip().split(","))))
    t1, t2 = max(combinations(tiles, r=2), key=lambda p: area(p[0], p[1]))
    print(area(t1, t2))
