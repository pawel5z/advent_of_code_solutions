from typing import List, Tuple, Dict, Set
import operator


def get_neighbours_of_same_type(garden: List[str], plot: Tuple[int, int]) -> List[Tuple[int, int]]:
    height = len(garden)
    width = len(garden[0])
    result = []
    plot_type = garden[plot[0]][plot[1]]

    for dr, dc in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        r, c = plot[0] + dr, plot[1] + dc
        if 0 <= r < height and 0 <= c < width and garden[r][c] == plot_type:
            result.append((r, c))

    return result


def get_neighbours_of_same_type_from_region(garden: List[str], plot: Tuple[int, int], region: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    height = len(garden)
    width = len(garden[0])
    result = []
    plot_type = garden[plot[0]][plot[1]]

    for dr, dc in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        r, c = plot[0] + dr, plot[1] + dc
        if 0 <= r < height and 0 <= c < width and garden[r][c] == plot_type and (r, c) in region:
            result.append((r, c))

    return result


def get_neighbours(plot: Tuple[int, int], height: int, width: int) -> Set[Tuple[int, int]]:
    result: Set[Tuple[int, int]] = set()

    for dr, dc in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        r, c = plot[0] + dr, plot[1] + dc
        if 0 <= r < height and 0 <= c < width:
            result.add((r, c))

    return result


def get_region(garden: List[str], start: Tuple[int, int]) -> Set[Tuple[int, int]]:
    visit_map: List[List[bool]] = [[False for plot in row] for row in garden]
    to_visit: Set[Tuple[int, int]] = set()
    to_visit.add(start)
    result: Set[Tuple[int, int]] = set()

    while len(to_visit) > 0:
        r, c = to_visit.pop()
        visit_map[r][c] = True
        result.add((r, c))

        for nr, nc in get_neighbours_of_same_type(garden, (r, c)):
            if not visit_map[nr][nc]:
                to_visit.add((nr, nc))

    return result


def enlarge_region_by_one(region: Set[Tuple[int, int]], height: int, width: int) -> Set[Tuple[int, int]]:
    result: Set[Tuple[int, int]] = set()

    for r, c in region:
        result.add((r, c))
        for dr, dc in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                result.add((nr, nc))

    return result

# TODO Identify which regions contain which.


def count_region_sides(garden: List[str], region: Set[Tuple[int, int]]) -> int:
    """Which is equivalent to counting regions's corners!

    Args:
        garden (List[str]): _description_
        region (Set[Tuple[int, int]]): _description_

    Returns:
        int: _description_
    """
    if len(region) == 0:
        return 4

    # enlarged_region = enlarge_region_by_one(region, len(garden), len(garden[0]))
    result = 0

    for r, c in region:
        # neighbours = get_neighbours_of_same_type_from_region(garden, (r, c), enlarged_region)
        neighbours = get_neighbours_of_same_type(garden, (r, c))
        match len(neighbours):
            case 1:
                result += 2
            case 2:
                if neighbours[0][0] != neighbours[1][0] and neighbours[0][1] != neighbours[1][1]:
                    result += 1

    return result


def get_fencing_price(garden: List[str]) -> int:
    result = 0
    visit_map: List[List[bool]] = [[False for _ in row] for row in garden]

    for r, row in enumerate(garden):
        for c, plot in enumerate(row):
            if visit_map[r][c]:
                continue

            region = get_region(garden, (r, c))
            for visited_r, visited_c in region:
                visit_map[visited_r][visited_c] = True

            result += len(region) * count_region_sides(garden, region)

    return result


if __name__ == "__main__":
    garden: List[str] = []

    while True:
        try:
            garden.append(input())
        except EOFError:
            break

    # print('\n'.join(garden))
    # print(get_unique_plot_types(garden))
    print(get_fencing_price(garden))
