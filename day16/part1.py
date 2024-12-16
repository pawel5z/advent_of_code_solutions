from typing import *
from math import inf
from itertools import chain, permutations


def rotate_clockwise(direction: Tuple[int, int]) -> Tuple[int, int]:
    match direction:
        case 0, 1:
            return (1, 0)
        case 1, 0:
            return (0, -1)
        case 0, -1:
            return (-1, 0)
        case -1, 0:
            return (0, 1)
        case _:
            raise ValueError


def rotate_counterclockwise(direction: Tuple[int, int]) -> Tuple[int, int]:
    match direction:
        case 1, 0:
            return (0, 1)
        case 0, -1:
            return (1, 0)
        case -1, 0:
            return (0, -1)
        case 0, 1:
            return (-1, 0)
        case _:
            raise ValueError


def find_type(board: List[List[str]], field_type: str) -> Optional[Tuple[int, int]]:
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == field_type:
                return (r, c)


def stringify_board(board: List[List[str]]) -> str:
    return '\n'.join(''.join(row) for row in board)


def get_lowest_score(board: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    costs: Dict[Tuple[Tuple[int, int], Tuple[int, int]], int] = {}

    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell != '#':
                for direction in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
                    costs[((r, c), direction)] = inf

    to_visit: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set()
    to_visit.add((start, (0, 1)))
    costs[(start, (0, 1))] = 0

    while len(to_visit) != 0:
        pos, direction = to_visit.pop()
        score = costs[(pos, direction)]

        r, c = pos[0] + direction[0], pos[1] + direction[1]
        if board[r][c] != '#' and score + 1 < costs[((r, c), direction)]:
            costs[((r, c), direction)] = score + 1
            to_visit.add(((r, c), direction))

        for new_dir in [rotate_clockwise(direction), rotate_counterclockwise(direction)]:
            if score + 1000 < costs[(pos, new_dir)]:
                costs[(pos, new_dir)] = score + 1000
                to_visit.add((pos, new_dir))

    return min(costs[(end, direction)] for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)])


if __name__ == '__main__':
    board: List[List[str]] = []

    while True:
        try:
            board.append(list(input()))
        except EOFError:
            break

    # print(stringify_board(board))
    start_pos = find_type(board, 'S')
    end_pos = find_type(board, 'E')
    print(get_lowest_score(board, start_pos, end_pos))
