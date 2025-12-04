import sys
import itertools


EMPTY = "."
OCCUPIED = "@"

def count_neighbours(diagram, x, y):
    width, height = len(diagram[0]), len(diagram)
    count = 0
    for dx, dy in itertools.product([-1, 0, 1], repeat=2):
        if dx == 0 and dy == 0:
            continue
        x1, y1 = x + dx, y + dy
        if not (0 <= x1 < width and 0 <= y1 < height):
            continue
        if diagram[y1][x1] == OCCUPIED:
            count += 1
    return count


if __name__ == "__main__":
    diagram = list(map(lambda line: list(line.strip()), sys.stdin.readlines()))
    total = 0
    changed = True
    while changed:
        changed = False
        for y, row in enumerate(diagram):
            for x, _ in enumerate(row):
                if diagram[y][x] == OCCUPIED and count_neighbours(diagram, x, y) < 4:
                    diagram[y][x] = EMPTY
                    total += 1
                    changed = True
    print(total)
