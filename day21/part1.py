from typing import List, Dict, Set, Tuple, Optional
from itertools import product, pairwise
from math import inf
import sys

Point = Tuple[int, int]

dpadcells: List[str] = '^v<>A'
numpadcells: List[str] = '0123456789A'

dpad: List[List[str]] = list(list(row) for row in '.^A\n<v>'.split())
numpad: List[List[str]] = list(list(row) for row in '789\n456\n123\n.0A'.split())


def get_walkable_fields(board: List[List[str]]) -> List[Point]:
    result: List[Point] = []

    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell != '.':
                result.append((r, c))

    return result


def find_type(board: List[List[str]], field_type: str) -> Optional[Point]:
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == field_type:
                return (r, c)


def get_neighbours(board: List[List[str]], pos: Point, height: int, width: int) -> List[Point]:
    result: List[Point] = []

    for dr, dc in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        r, c = pos[0] + dr, pos[1] + dc
        if 0 <= r < height and 0 <= c < width and board[r][c] != '.':
            result.append((r, c))

    return result


def fw(board: List[List[str]]) -> Tuple[
    Dict[Tuple[Point, Point], int],
    Dict[Tuple[Point, Point], Optional[Point]]
]:
    """Floyd-Warshall with path reconstruction
    """
    dist: Dict[Tuple[Point, Point], int] = {}
    prev: Dict[Tuple[Point, Point], Optional[Point]] = {}
    walkable_fields: List[Point] = get_walkable_fields(board)

    for pos1, pos2 in product(walkable_fields, repeat=2):
        dist[pos1, pos2] = inf
        prev[pos1, pos2] = None

    height, width = len(board), len(board[0])

    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == '.':
                continue

            dist[(r, c), (r, c)] = 0
            prev[(r, c), (r, c)] = (r, c)

            for nr, nc in get_neighbours(board, (r, c), height, width):
                dist[(r, c), (nr, nc)] = 1
                prev[(r, c), (nr, nc)] = (r, c)

    for k in walkable_fields:
        for i in walkable_fields:
            for j in walkable_fields:
                if dist[i, j] > dist[i, k] + dist[k, j]:
                    dist[i, j] = dist[i, k] + dist[k, j]
                    prev[i, j] = prev[k, j]

                    if not (i[0] == k[0] == j[0] or i[1] == k[1] == j[1]):
                        dist[i, j] += 1

    return dist, prev


def reconstruct_path(start: Point, end: Point, prev: Dict[Tuple[Point, Point], Optional[Point]]) -> List[Point]:
    if prev[start, end] is None:
        return []

    result: List[Point] = []
    result.append(end)
    node = tuple(end)

    while start != node:
        node = prev[start, node]
        result.append(node)

    result.reverse()
    return result


def path_heuristic(path: List[Point]) -> int:
    """Adds a penalty of each direction change along specified path.
    """
    if len(path) == 0:
        return inf

    result: int = 0

    for i in range(len(path) - 2):
        n1, n2, n3 = tuple(path[i:i + 3])
        if not (n1[0] == n2[0] == n3[0] or n1[1] == n2[1] == n3[1]):
            result += 1

    return result


def get_numeric_part(code: str) -> int:
    return int(''.join(filter(lambda char: char in '0123456789', code)))


def direction_to_key(direction: Point) -> str:
    match direction:
        case 0, 1:
            return '>'
        case 1, 0:
            return 'v'
        case -1, 0:
            return '^'
        case 0, -1:
            return '<'
        case _:
            raise ValueError


def compute_directions(positions: List[Point]) -> List[Point]:
    result: List[Point] = []

    for pos1, pos2 in pairwise(positions):
        result.append((pos2[0] - pos1[0], pos2[1] - pos1[1]))

    return result


def get_move_sequence(
    prev: Dict[Tuple[Point, Point], Optional[Point]],
    hover: Point,
    target: Point
) -> List[Point]:
    return reconstruct_path(hover, target, prev)


if __name__ == '__main__':
    # print(dpad)
    # print(numpad)
    dpad_dist, dpad_prev = fw(dpad)
    numpad_dist, numpad_prev = fw(numpad)
    result: int = 0

    for code in map(lambda line: line.strip(), sys.stdin.readlines()):
        hover_pos: Point = find_type(numpad, 'A')
        numpad_moves: List[str] = []

        for key in code:
            key_pos = find_type(numpad, key)
            numpad_moves += list(map(direction_to_key,
                                 compute_directions(get_move_sequence(numpad_prev, hover_pos, key_pos))))
            numpad_moves.append('A')
            hover_pos = key_pos

        # print(''.join(numpad_moves))
        # print(len(numpad_moves))
        hover_pos: Point = find_type(dpad, 'A')
        dpad1_moves: List[str] = []

        for key in numpad_moves:
            key_pos = find_type(dpad, key)
            dpad1_moves += list(map(direction_to_key,
                                    compute_directions(get_move_sequence(dpad_prev, hover_pos, key_pos))))
            dpad1_moves.append('A')
            hover_pos = key_pos

        # print(''.join(dpad1_moves))
        # print(len(dpad1_moves))
        hover_pos: Point = find_type(dpad, 'A')
        dpad2_moves: List[str] = []

        for key in dpad1_moves:
            key_pos = find_type(dpad, key)
            dpad2_moves += list(map(direction_to_key,
                                    compute_directions(get_move_sequence(dpad_prev, hover_pos, key_pos))))
            dpad2_moves.append('A')
            hover_pos = key_pos

        # print(''.join(dpad2_moves))
        # print(len(dpad2_moves))
        result += len(dpad2_moves) * get_numeric_part(code)

    print(result)
