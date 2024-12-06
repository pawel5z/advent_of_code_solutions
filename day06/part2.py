from typing import List, Tuple, Set
import itertools


class LoopError(BaseException):
    pass


def pretty_print_map():
    print(*map(lambda row: ''.join(row), lab_map), sep='\n')


def get_guard_position(map: List[List[str]]) -> Tuple[int, int]:
    for r, row in enumerate(map):
        for c, col in enumerate(row):
            if col == '^':
                return (r, c)

    raise RuntimeError


def is_inside_map(pos: Tuple[int, int], width: int, height: int) -> bool:
    return 0 <= pos[0] < height and 0 <= pos[1] < width


def rotate_90_degrees(dir: Tuple[int, int]) -> Tuple[int, int]:
    match dir:
        case 0, -1:
            return (-1, 0)
        case 1, 0:
            return (0, -1)
        case 0, 1:
            return (1, 0)
        case -1, 0:
            return (0, 1)
        case _:
            raise RuntimeError


def simulate_guard_path(map: List[List[str]]):
    pos = get_guard_position(map)
    dir = (-1, 0)

    width, height = len(map[0]), len(map)

    steps_count = 0
    while True:
        map[pos[0]][pos[1]] = 'X'
        new_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if not is_inside_map(new_pos, width, height):
            break
        if steps_count >= width * height * 2:  # heavy heuristic, should be done better
            raise LoopError
        if map[new_pos[0]][new_pos[1]] == '#':
            dir = rotate_90_degrees(dir)
            continue
        pos = new_pos
        steps_count += 1


def count_obstacles_causing_loops(map: List[List[str]]) -> int:
    width, height = len(map[0]), len(map)
    candidates = set(itertools.product(range(width), range(height)))
    candidates.remove(get_guard_position(map))
    result = 0

    for candidate in candidates:
        map_copy = [list(row) for row in map]
        map_copy[candidate[0]][candidate[1]] = '#'
        try:
            simulate_guard_path(map_copy)
        except LoopError:
            result += 1

    return result


if __name__ == "__main__":
    lab_map: List[List[str]] = []

    while True:
        try:
            lab_map.append(list(input()))
        except EOFError:
            break

    print(count_obstacles_causing_loops(lab_map))
