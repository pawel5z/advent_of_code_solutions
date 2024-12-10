from typing import List, Tuple


def get_trailhead_score(row: int, col: int, topographic_map: List[List[int]]):
    """Get number of achievable points of elevation nine.

    Args:
        row (int): _description_
        col (int): _description_
        topographic_map (List[List[int]]): _description_

    Returns:
        _type_: _description_
    """
    to_visit: List[Tuple[int, int]] = [(row, col)]
    result = 0
    height = len(topographic_map)
    width = len(topographic_map[0])
    visited: List[List[bool]] = [[False for col in row] for row in topographic_map]

    while len(to_visit) > 0:
        v_row, v_col = to_visit.pop(0)

        if visited[v_row][v_col]:
            continue

        visited[v_row][v_col] = True
        elevation = topographic_map[v_row][v_col]

        if elevation == 9:
            result += 1
            continue

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row = v_row + dr
            new_col = v_col + dc
            if 0 <= new_row < height and 0 <= new_col < width and topographic_map[new_row][new_col] - 1 == elevation:
                to_visit.append((new_row, new_col))

    return result


if __name__ == '__main__':
    topographic_map: List[List[int]] = []

    while True:
        try:
            topographic_map.append(list(map(int, input())))
        except EOFError:
            break

    # print(topographic_map)
    result = 0

    for r, row in enumerate(topographic_map):
        for c, elevation in enumerate(row):
            if elevation == 0:
                result += get_trailhead_score(r, c, topographic_map)

    print(result)
