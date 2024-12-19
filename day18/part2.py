from typing import *
from math import inf
import sys
from tqdm import tqdm

SIZE = 70


def get_neighbours(board: List[List[str]], pos: Tuple[int, int], height: int, width: int) -> List[Tuple[int, int]]:
    result: List[Tuple[int, int]] = []

    for dr, dc in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        r, c = pos[0] + dr, pos[1] + dc
        if 0 <= r < height and 0 <= c < width and board[r][c] == '.':
            result.append((r, c))

    return result


def stringify_board(board: List[List[str]]) -> str:
    return '\n'.join(''.join(row) for row in board)


def is_reachable(board: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> bool:
    visited: Set[Tuple[int, int]] = set()
    to_visit: Set[Tuple[int, int]] = set()

    height = len(board)
    width = len(board[0])
    to_visit.add(start)

    while len(to_visit) != 0:
        pos = to_visit.pop()
        visited.add(pos)

        for r, c in get_neighbours(board, pos, height, width):
            if (r, c) == end:
                return True

            if (r, c) not in visited:
                to_visit.add((r, c))
                continue

    return False


if __name__ == '__main__':
    board: List[List[str]] = [['.' for _ in range(SIZE+1)] for _ in range(SIZE + 1)]
    # print(stringify_board(board))

    for line in tqdm(sys.stdin.readlines()):
        c, r = tuple(map(int, line.split(',')))
        board[r][c] = '#'

        if not is_reachable(board, (0, 0), (SIZE, SIZE)):
            print(f'{c},{r}')
            break
