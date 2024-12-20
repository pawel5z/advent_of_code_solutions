from typing import *
from math import inf
import sys
from tqdm import tqdm


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


def get_cheat_fields_around(board: List[List[str]], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    result: List[Tuple[int, int]] = []
    height: int = len(board)
    width: int = len(board)

    for dr, dc in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        r, c = pos[0] + dr, pos[1] + dc
        if 0 <= r < height and 0 <= c < width:  # and board[r][c] == '#':
            result.append((r, c))

    return result


def get_cheats(board: List[List[str]], pos: Tuple[int, int]) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    result: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

    for cheat_field1 in get_cheat_fields_around(board, pos):
        # result.append((pos, cheat_field1))
        if board[cheat_field1[0]][cheat_field1[1]] != '#':
            continue

        for cheat_field2 in get_cheat_fields_around(board, cheat_field1):
            if cheat_field1 != cheat_field2 and board[cheat_field2[0]][cheat_field2[1]] != '#':
                result.append((cheat_field1, cheat_field2))

    return result


def apply_cheat(board: List[List[str]], cheat_start: Tuple[int, int], cheat_end: Tuple[int, int]) -> List[List[str]]:
    result: List[List[str]] = [list(row) for row in board]
    result[cheat_start[0]][cheat_start[1]] = '1'
    result[cheat_end[0]][cheat_end[1]] = '2'
    return result


def stringify_board(board: List[List[str]]) -> str:
    return '\n'.join(''.join(row) for row in board)


def get_shortest_path_length(board: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    costs: Dict[Tuple[int, int], int] = {}
    to_visit: Set[Tuple[int, int]] = set()

    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell != '#':
                costs[r, c] = inf
                to_visit.add((r, c))

    costs[start] = 0
    height = len(board)
    width = len(board[0])

    while len(to_visit) != 0:
        pos = min(to_visit, key=lambda p: costs[p])

        if pos == end:
            return costs[end]

        to_visit.remove(pos)
        score = costs[pos]

        for r, c in get_neighbours(board, pos, height, width):
            if (r, c) not in to_visit:
                continue

            if board[pos[0]][pos[1]] == '1' and board[r][c] != '2':
                continue

            if score + 1 < costs[r, c]:
                costs[r, c] = score + 1

    return costs[end]


if __name__ == '__main__':
    board: List[List[str]] = [list(row.strip()) for row in sys.stdin.readlines()]
    start: str = find_type(board, 'S')
    end: str = find_type(board, 'E')
    original_length = get_shortest_path_length(board, start, end)
    print(f'original length: {original_length}')
    sys.exit()
    # print(stringify_board(board))
    # applied_cheats: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set()
    result = 0
    cheat_stats: Dict[int, int] = {}
    all_cheats: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set()

    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell != '#':
                all_cheats.update(get_cheats(board, (r, c)))

    for cheat_start, cheat_end in tqdm(all_cheats):
        cheated_board = apply_cheat(board, cheat_start, cheat_end)
        delta = original_length - get_shortest_path_length(cheated_board, start, end)

        if delta >= 100:
            if delta not in cheat_stats.keys():
                cheat_stats[delta] = 0
            cheat_stats[delta] += 1
            result += 1
            # print(stringify_board(cheated_board))
            # print()

    print(cheat_stats)
    print(result)
