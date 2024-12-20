from typing import *
from math import inf
import sys
from tqdm import tqdm
from itertools import product


def find_type(board: List[List[str]], field_type: str) -> Optional[Tuple[int, int]]:
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == field_type:
                return (r, c)


def get_neighbours(board: List[List[str]], pos: Tuple[int, int], height: int, width: int) -> List[Tuple[int, int]]:
    result: List[Tuple[int, int]] = []

    for dr, dc in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        r, c = pos[0] + dr, pos[1] + dc
        if 0 <= r < height and 0 <= c < width and board[r][c] != '#':
            result.append((r, c))

    return result


def get_cheats(board: List[List[str]]) -> Set[Tuple[Tuple[int, int], Tuple[int, int]]]:
    result: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set()
    height, width = len(board), len(board[0])

    for (r1, c1), (r2, c2) in tqdm(product(product(range(height), range(width)), repeat=2)):
        if not (1 <= abs(c2 - c1) + abs(r2 - r1) <= 19):
            continue

        if board[r2][c2] == '#':
            continue

        result.add(((r1, c1), (r2, c2)))

    # for r1, row1 in enumerate(board):
    #     for c1, cell1 in enumerate(row1):
    #         for r2, row2 in enumerate(board):
    #             for c2, cell2 in enumerate(row2):
    #                 if not (1 <= abs(c2 - c1) + abs(r2 - r1) <= 1):
    #                     continue

    #                 if board[r2][c2] == '#':
    #                     continue

    #                 result.add(((r1, c1), (r2, c2)))

    return result


def stringify_board(board: List[List[str]]) -> str:
    return '\n'.join(''.join(row) for row in board)


def get_shortest_path_lengths(board: List[List[str]], start: Tuple[int, int]) -> Dict[Tuple[int, int], int]:
    costs: Dict[Tuple[int, int], int] = {}
    to_visit: Set[Tuple[int, int]] = set()

    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell != '#':
                costs[r, c] = inf
                to_visit.add((r, c))

    costs[start] = 0
    height, width = len(board), len(board[0])

    while len(to_visit) != 0:
        pos = min(to_visit, key=lambda p: costs[p])

        to_visit.remove(pos)
        score = costs[pos]

        for r, c in get_neighbours(board, pos, height, width):
            if (r, c) not in to_visit:
                continue

            if score + 1 < costs[r, c]:
                costs[r, c] = score + 1

    return costs


if __name__ == '__main__':
    board: List[List[str]] = [list(row.strip()) for row in sys.stdin.readlines()]
    start: str = find_type(board, 'S')
    end: str = find_type(board, 'E')
    costs = get_shortest_path_lengths(board, start)
    original_length = costs[end]
    print(f'original length: {original_length}')
    # print(stringify_board(board))
    result = 0
    cheat_stats: Dict[int, int] = {}
    print('searching for cheats...')
    all_cheats: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = get_cheats(board)
    print(f'obtained list of cheats: {len(all_cheats)} cheats total')

    height, width = len(board), len(board[0])

    for cheat_start, cheat_end in tqdm(all_cheats):
        cheat_start_cost = inf

        if cheat_start in costs.keys():
            cheat_start_cost = costs[cheat_start]
        else:
            cheat_start_cost = min(
                (costs[neighbour] for neighbour in get_neighbours(
                    board, cheat_start, height, width) if neighbour != cheat_end),
                default=inf) + 1

        if cheat_start_cost == inf:
            continue

        cost_with_cheat = original_length - costs[cheat_end] + cheat_start_cost + \
            abs(cheat_end[1] - cheat_start[1]) + abs(cheat_end[0] - cheat_start[0])

        delta = original_length - cost_with_cheat

        if delta >= 50:
            if delta not in cheat_stats.keys():
                cheat_stats[delta] = 0
            cheat_stats[delta] += 1
            result += 1
            # print(stringify_board(cheated_board))
            # print()

    for k in sorted(cheat_stats.keys()):
        print(f'There are {cheat_stats[k]} cheats that save {k} picoseconds.')

    print(result)
