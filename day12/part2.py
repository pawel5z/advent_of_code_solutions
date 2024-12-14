from typing import List, Tuple, Dict, Set
import operator
import itertools


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


def get_neighbouring_corners(plot: Tuple[int, int], height: int, width: int) -> List[Tuple[int, int]]:
    result = []

    for dr, dc in itertools.product([-1, 1], repeat=2):
        r, c = plot[0] + dr, plot[1] + dc
        if 0 <= r < height and 0 <= c < width:
            result.append((r, c))

    return result


def count_foreign_plots_between_neighbours(garden: List[str], plot: Tuple[int, int], neighbours: List[Tuple[int, int]]) -> int:
    result = 0
    plot_type = garden[plot[0]][plot[1]]
    corner_neighbours = get_neighbouring_corners(plot, len(garden), len(garden[0]))

    for n1, n2 in itertools.combinations(neighbours, 2):
        for corner_neighbour in corner_neighbours:
            if garden[corner_neighbour[0]][corner_neighbour[1]] == plot_type:
                continue

            if (n1[1] == corner_neighbour[1] and n2[0] == corner_neighbour[0]) or (n2[1] == corner_neighbour[1] and n1[0] == corner_neighbour[0]):
                result += 1

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


def count_region_sides(garden: List[str], region: Set[Tuple[int, int]]) -> int:
    """Which is equivalent to counting regions's corners!

    Args:
        garden (List[str]): _description_
        region (Set[Tuple[int, int]]): _description_

    Returns:
        int: _description_
    """
    if len(region) == 1:
        return 4

    result = 0

    for r, c in region:
        neighbours = get_neighbours_of_same_type(garden, (r, c))
        match len(neighbours):
            case 1:
                result += 2
            case 2:
                if neighbours[0][0] == neighbours[1][0] or neighbours[0][1] == neighbours[1][1]:
                    continue

                result += 1
                result += count_foreign_plots_between_neighbours(garden, (r, c), neighbours)
            case 3 | 4:
                result += count_foreign_plots_between_neighbours(garden, (r, c), neighbours)

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
