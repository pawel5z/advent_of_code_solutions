import numpy as np
from typing import List, Set, Tuple
import re


def gcd(a: int, b: int) -> int:
    if b == 0:
        return a
    return gcd(b, a % b)


def get_antenna_types(antenna_map: List[str]) -> Set[str]:
    result: Set[str] = set()
    for row in antenna_map:
        for cell in row:
            if re.match(r'\w', cell):
                result.add(cell)
    return result


def get_antenna_type_positions(antenna_map: List[str], antenna_type: str) -> List[Tuple[int, int]]:
    result: List[np.ndarray] = []
    for r, row in enumerate(antenna_map):
        for c, cell in enumerate(row):
            if cell == antenna_type:
                result.append((r, c))
    return result


def is_in_map_bounds(pos: Tuple[int, int], width: int, height: int) -> bool:
    return 0 <= pos[0] < height and 0 <= pos[1] < width


def is_twice_as_far(diff1: Tuple[int, int], diff2: Tuple[int, int]) -> bool:
    return (diff1[0] == 2 * diff2[0] and diff1[1] == 2 * diff2[1]) or (diff1[0] * 2 == diff2[0] and diff1[1] * 2 == diff2[1])


def is_antinode(pos: Tuple[int, int], a1: Tuple[int, int], a2: Tuple[int, int]) -> bool:
    diff1 = (a1[0] - pos[0], a1[1] - pos[1])
    diff2 = (a2[0] - pos[0], a2[1] - pos[1])
    return is_twice_as_far(diff1, diff2) or is_twice_as_far((-diff1[0], -diff1[1]), diff2)


def get_antinode_locations(a1: Tuple[int, int], a2: Tuple[int, int], width: int, height: int) -> List[Tuple[int, int]]:
    diff = (a2[0] - a1[0], a2[1] - a1[1])
    divisor = gcd(abs(diff[0]), abs(diff[1]))
    diff = (diff[0] / divisor, diff[1] / divisor)
    result: List[Tuple[int, int]] = []

    pos = a1
    while is_in_map_bounds(pos, width, height):
        if is_antinode(pos, a1, a2):
            result.append(pos)
            break
        pos = (pos[0] + diff[0], pos[1] + diff[1])

    diff = (-diff[0], -diff[1])
    pos = a2
    while is_in_map_bounds(pos, width, height):
        if is_antinode(pos, a1, a2):
            result.append(pos)
            break
        pos = (pos[0] + diff[0], pos[1] + diff[1])

    return result


def count_unique_antinode_locations(antenna_map: List[str], antenna_types: Set[str]) -> int:
    antinode_locations: Set[Tuple[int, int]] = set()

    for antenna_type in antenna_types:
        antenna_positions = get_antenna_type_positions(antenna_map, antenna_type)
        for i, a1 in enumerate(antenna_positions[:-1]):
            for a2 in antenna_positions[i+1:]:
                for detected_antinode in get_antinode_locations(a1, a2, len(antenna_map[0]), len(antenna_map)):
                    antinode_locations.add(detected_antinode)

    return len(antinode_locations)


if __name__ == "__main__":
    antenna_map: List[str] = []

    while True:
        try:
            antenna_map.append(input())
        except EOFError:
            break

    print(count_unique_antinode_locations(antenna_map, get_antenna_types(antenna_map)))
