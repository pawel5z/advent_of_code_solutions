import re
from typing import Set, Tuple, List
import functools

WIDTH = 101
# WIDTH = 11
HEIGHT = 103
# HEIGHT = 7
TIME = 100

if __name__ == '__main__':
    quadrants_count: List[int] = [0] * 4

    while True:
        try:
            match = re.match(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', input())
            px, py, vx, vy = map(int, match.groups())
            final_px = (px + vx * TIME) % WIDTH
            final_py = (py + vy * TIME) % HEIGHT

            if final_px < WIDTH // 2 and final_py < HEIGHT // 2:
                quadrants_count[0] += 1
            elif final_px < WIDTH // 2 and HEIGHT // 2 < final_py:
                quadrants_count[1] += 1
            elif WIDTH // 2 < final_px and final_py < HEIGHT // 2:
                quadrants_count[2] += 1
            elif WIDTH // 2 < final_px and HEIGHT // 2 < final_py:
                quadrants_count[3] += 1
        except EOFError:
            break

    print(functools.reduce(lambda a, b: a * b, quadrants_count, 1))
