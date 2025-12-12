import sys
from itertools import combinations


def area(t1: tuple[int, int], t2: tuple[int, int]) -> bool:
    return (abs(t1[0]-t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)


def is_vertical(t1: tuple[int, int], t2: tuple[int, int]) -> bool:
    return t1[0] == t2[0]


def is_facing_right(t1: tuple[int, int], t2: tuple[int, int]) -> bool:
    return t2[1] - t1[1] < 0


def does_rectangle_fit(t1: tuple[int, int], t2: tuple[int, int], segments: list[list[tuple[int, int]]]) -> bool:
    left, right, top, bottom = min(t1[0], t2[0]), max(t1[0], t2[0]), min(t1[1], t2[1]), max(t1[1], t2[1])
    for y in range(top, bottom + 1):
        covered = False
        for segment in segments[y]:
            if segment[0] <= left and right <= segment[1]:
                covered = True
                break
        if not covered:
            return False
    return True


if __name__ == "__main__":
    NO_BOUND = -1
    tiles = []
    for line in sys.stdin.readlines():
        tiles.append(tuple(map(int, line.strip().split(","))))
    # zero-align
    left, top = min(map(lambda t: t[0], tiles)), min(map(lambda t: t[1], tiles))
    tiles = [(t[0] - left, t[1] - top) for t in tiles]

    lines: tuple[tuple[int, int], tuple[int, int]] = [(tiles[i], tiles[i+1]) for i in range(-1, len(tiles) - 1)]
    bottom = max(map(lambda t: t[1], tiles))
    # segment list index is simultaneously Y coordinate
    segments: list[list[tuple[int, int]]] = [[] for _ in range(bottom + 1)]
    # left bounds
    for line in lines:
        if not is_vertical(line[0], line[1]) or not is_facing_right(line[0], line[1]):
            continue
        for tile_y in range(line[1][1], line[0][1] + 1):
            segments[tile_y].append((line[0][0], NO_BOUND))
    # right bounds
    for line in lines:
        if not is_vertical(line[0], line[1]) or is_facing_right(line[0], line[1]):
            continue
        for tile_y in range(line[0][1], line[1][1] + 1):
            for i, segment in enumerate(segments[tile_y]):
                if segment[1] == NO_BOUND or segment[0] < line[0][0]:
                    segments[tile_y][i] = (segment[0], line[0][0])
    # merge overlapping segments
    for y, _ in enumerate(segments):
        segments[y] = sorted(segments[y], key=lambda segment: segment[0])
        i = 0
        while i < len(segments[y]) - 1:
            if segments[y][i][1] >= segments[y][i+1][0]:
                segments[y][i] = (segments[y][i][0], segments[y][i+1][1])
                segments[y].pop(i+1)
            else:
                i += 1

    # for segments_y in segments:
    #     print(segments_y)

    t1, t2 = max(
        filter(lambda p: does_rectangle_fit(p[0], p[1], segments), combinations(tiles, r=2)),
        key=lambda p: area(p[0], p[1])
    )
    print(area(t1, t2))
