from typing import *
from math import inf

SIZE = 70
COUNT = 1024


def get_neighbours(board: List[List[str]], pos: Tuple[int, int], height: int, width: int) -> List[Tuple[int, int]]:
    result: List[Tuple[int, int]] = []

    for dr, dc in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        r, c = pos[0] + dr, pos[1] + dc
        if 0 <= r < height and 0 <= c < width and board[r][c] == '.':
            result.append((r, c))

    return result


def stringify_board(board: List[List[str]]) -> str:
    return '\n'.join(''.join(row) for row in board)


def get_shortest_path_length(board: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    costs: Dict[Tuple[int, int], int] = {}
    to_visit: Set[Tuple[int, int]] = set()

    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == '.':
                costs[r, c] = inf
                to_visit.add((r, c))

    costs[start] = 0
    height = len(board)
    width = len(board[0])

    while len(to_visit) != 0:
        pos = min(to_visit, key=lambda p: costs[p])
        to_visit.remove(pos)
        score = costs[pos]

        for r, c in get_neighbours(board, pos, height, width):
            if (r, c) not in to_visit:
                continue

            if score + 1 < costs[r, c]:
                costs[r, c] = score + 1

    return costs[end]


if __name__ == '__main__':
    board: List[List[str]] = [['.' for _ in range(SIZE+1)] for _ in range(SIZE + 1)]

    for _ in range(COUNT):
        c, r = tuple(map(int, input().split(',')))
        board[r][c] = '#'

    # print(stringify_board(board))
    print(get_shortest_path_length(board, (0, 0), (SIZE, SIZE)))
