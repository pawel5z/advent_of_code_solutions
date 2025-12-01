from typing import *


def get_robot(warehouse: List[List[str]]) -> Tuple[int, int]:
    for r, row in enumerate(warehouse):
        for c, col in enumerate(row):
            if col == '@':
                return (r, c)


def move(warehouse: List[List[str]], robot: Tuple[int, int], move: str) -> Tuple[int, int]:
    match move:
        case '^':
            dr, dc = (-1, 0)
        case 'v':
            dr, dc = (1, 0)
        case '<':
            dr, dc = (0, -1)
        case '>':
            dr, dc = (0, 1)
        case _:
            return robot

    final_r, final_c = robot[0] + dr, robot[1] + dc

    while warehouse[final_r][final_c] not in ['#', '.']:
        final_r, final_c = final_r + dr, final_c + dc

    if warehouse[final_r][final_c] == '#':
        return robot

    r, c = final_r, final_c

    while (r, c) != robot:
        warehouse[r][c] = warehouse[r - dr][c - dc]
        r, c = r - dr, c - dc

    warehouse[r][c] = '.'
    return (robot[0] + dr, robot[1] + dc)


def warehouse_gps(warehouse: List[List[str]]) -> Iterator[int]:
    for r, row in enumerate(warehouse):
        for c, col in enumerate(row):
            if col == 'O':
                yield 100 * r + c


def prettify_warehouse(warehouse: List[List[str]]) -> str:
    return '\n'.join(''.join(row) for row in warehouse)


if __name__ == '__main__':
    warehouse: List[List[str]] = []
    input_string = input()

    while input_string != '':
        warehouse.append(list(input_string))
        input_string = input()

    moves = []

    while True:
        try:
            moves.append(input())
        except EOFError:
            break

    moves = ''.join(moves)
    robot = get_robot(warehouse)

    for m in moves:
        robot = move(warehouse, robot, m)

    # print(prettify_warehouse(warehouse))
    print(sum(warehouse_gps(warehouse)))
