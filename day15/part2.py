from typing import *


def transform_warehouse(warehouse: List[List[str]]) -> List[List[str]]:
    result = []

    for row in warehouse:
        new_row: List[str] = []

        for col in row:
            match col:
                case '#':
                    new_row.append('#')
                    new_row.append('#')
                case 'O':
                    new_row.append('[')
                    new_row.append(']')
                case '.':
                    new_row.append('.')
                    new_row.append('.')
                case '@':
                    new_row.append('@')
                    new_row.append('.')

        result.append(new_row)

    return result


def get_robot(warehouse: List[List[str]]) -> Tuple[int, int]:
    for r, row in enumerate(warehouse):
        for c, col in enumerate(row):
            if col == '@':
                return (r, c)


def movable(warehouse: List[List[str]], pos: Tuple[int, int], dir: Tuple[int, int]) -> bool:
    field_type = warehouse[pos[0]][pos[1]]

    match field_type:
        case '.':
            return True
        case '#':
            return False
        case '@':
            return movable(warehouse, (pos[0] + dir[0], pos[1] + dir[1]), dir)
        case '[':
            if dir[0] == 0:
                # horizontal movement
                return movable(warehouse, (pos[0], pos[1] + 2 * dir[1]), dir)
            else:
                # vertical movement
                return movable(warehouse, (pos[0] + dir[0], pos[1]), dir) and movable(warehouse, (pos[0] + dir[0], pos[1] + 1), dir)
        case ']':
            if dir[0] == 0:
                # horizontal movement
                return movable(warehouse, (pos[0], pos[1] + 2 * dir[1]), dir)
            else:
                # vertical movement
                return movable(warehouse, (pos[0] + dir[0], pos[1]), dir) and movable(warehouse, (pos[0] + dir[0], pos[1] - 1), dir)

    raise ValueError


def perform_move(warehouse: List[List[str]], pos: Tuple[int, int], dir: Tuple[int, int]):
    field_type = warehouse[pos[0]][pos[1]]

    match field_type:
        case '.':
            warehouse[pos[0]][pos[1]] = warehouse[pos[0] - dir[0]][pos[1] - dir[1]]
            return
        case '@':
            perform_move(warehouse, (pos[0] + dir[0], pos[1] + dir[1]), dir)
            warehouse[pos[0]][pos[1]] = '.'
            return
        case '[':
            if dir[0] == 0:
                # horizontal movement
                perform_move(warehouse, (pos[0], pos[1] + dir[1]), dir)
                warehouse[pos[0]][pos[1]] = warehouse[pos[0]][pos[1] - dir[1]]
            else:
                # vertical movement
                perform_move(warehouse, (pos[0] + dir[0], pos[1]), dir)
                perform_move(warehouse, (pos[0] + dir[0], pos[1] + 1), dir)
                warehouse[pos[0]][pos[1]] = warehouse[pos[0] - dir[0]][pos[1]]
                warehouse[pos[0]][pos[1] + 1] = '.'
            return
        case ']':
            if dir[0] == 0:
                # horizontal movement
                perform_move(warehouse, (pos[0], pos[1] + dir[1]), dir)
                warehouse[pos[0]][pos[1]] = warehouse[pos[0]][pos[1] - dir[1]]
            else:
                # vertical movement
                perform_move(warehouse, (pos[0] + dir[0], pos[1]), dir)
                perform_move(warehouse, (pos[0] + dir[0], pos[1] - 1), dir)
                warehouse[pos[0]][pos[1]] = warehouse[pos[0] - dir[0]][pos[1]]
                warehouse[pos[0]][pos[1] - 1] = '.'
            return

    raise ValueError


def eval_move(warehouse: List[List[str]], robot: Tuple[int, int], move: str) -> Tuple[int, int]:
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

    if not movable(warehouse, robot, (dr, dc)):
        return robot

    perform_move(warehouse, robot, (dr, dc))
    return (robot[0] + dr, robot[1] + dc)


def warehouse_gps(warehouse: List[List[str]]) -> Iterator[int]:
    for r, row in enumerate(warehouse):
        for c, col in enumerate(row):
            if col == '[':
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
    warehouse = transform_warehouse(warehouse)
    # print(prettify_warehouse(warehouse))
    robot = get_robot(warehouse)

    for m in moves:
        # print(f'\nMove {m}:')
        robot = eval_move(warehouse, robot, m)
        # print(prettify_warehouse(warehouse))

    # print(prettify_warehouse(warehouse))
    print(sum(warehouse_gps(warehouse)))
