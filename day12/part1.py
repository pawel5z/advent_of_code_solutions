from typing import List, Tuple, Dict, Set


def get_unique_plot_types(garden: List[str]) -> Set[str]:
    result = set()

    for row in garden:
        for plot in row:
            result.add(plot)

    return result


def get_neighbours(garden: List[str], plot: Tuple[int, int]) -> List[Tuple[int, int]]:
    height = len(garden)
    width = len(garden[0])
    result = []
    plot_type = garden[plot[0]][plot[1]]

    for dr, dc in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        r, c = plot[0] + dr, plot[1] + dc
        if 0 <= r < height and 0 <= c < width and garden[r][c] == plot_type:
            result.append((r, c))

    return result


def get_region(garden: List[str], start: Tuple[int, int]) -> Set[Tuple[int, int]]:
    visit_map: List[List[bool]] = [[False for plot in row] for row in garden]
    plot_type = garden[start[0]][start[1]]
    to_visit: Set[Tuple[int, int]] = set()
    to_visit.add(start)
    result: Set[Tuple[int, int]] = set()

    while len(to_visit) > 0:
        r, c = to_visit.pop()
        visit_map[r][c] = True
        result.add((r, c))

        for nr, nc in get_neighbours(garden, (r, c)):
            if not visit_map[nr][nc]:
                to_visit.add((nr, nc))

    return result


def get_region_perimeter(garden: List[str], region: Set[Tuple[int, int]]) -> int:
    result = len(region) * 4

    for r, c in region:
        result -= len(get_neighbours(garden, (r, c)))

    return result


def get_fencing_price(garden: List[str]) -> int:
    result = 0
    visit_map: List[List[bool]] = [[False for plot in row] for row in garden]

    for r, row in enumerate(garden):
        for c, plot in enumerate(row):
            if visit_map[r][c]:
                continue

            region = get_region(garden, (r, c))
            for visited_r, visited_c in region:
                visit_map[visited_r][visited_c] = True

            result += len(region) * get_region_perimeter(garden, region)

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
