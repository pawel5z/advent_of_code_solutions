import re
from typing import Set, Tuple, List
import functools

WIDTH = 101
HEIGHT = 103


def get_area_map(robots: List[Tuple[int, int, int, int]]) -> List[str]:
    area_map: List[List[str]] = [[' '] * WIDTH for _ in range(HEIGHT)]

    for (px, py, _, _) in robots:
        area_map[py][px] = '█'

    return [''.join(row) for row in area_map]


def forward(robots: List[Tuple[int, int, int, int]]):
    for i, (px, py, vx, vy) in enumerate(robots):
        new_px = (px + vx) % WIDTH
        new_py = (py + vy) % HEIGHT
        robots[i] = (new_px, new_py, vx, vy)


def maybe_christmas_tree(area_map: List[str]) -> bool:
    """Hopeful heuristic.

    Args:
        area_map (List[str]): _description_

    Returns:
        bool: _description_
    """
    for row in area_map:
        if re.search(r'█{10,}', row):
            return True
    return False


if __name__ == '__main__':
    robots: List[Tuple[int, int, int, int]] = []

    with open('./day14/puzzle.input') as f:
        while True:
            try:
                input_string = f.readline()
                if input_string == '':
                    break
                match = re.match(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', input_string)
                px, py, vx, vy = map(int, match.groups())
                px = px % WIDTH
                py = py % HEIGHT
                robots.append((px, py, vx, vy))
            except EOFError:
                break

    i = 0
    while True:
        if i % 10_000 == 0:
            print(i)
        area_map = get_area_map(robots)
        if maybe_christmas_tree(area_map):
            if i % 10_000 != 0:
                print(i)
            print('\n'.join(area_map))
            input()
        forward(robots)
        i += 1
