def count_paths(src: str, dst: str, neighbors: dict[str, list[str]]) -> int:
    path_counts: dict[str, int] = {src: 1}
    queue: list[str] = [src]

    while queue:
        current = queue.pop(0)
        for neighbor in neighbors[current]:
            if neighbor not in path_counts:
                queue.append(neighbor)
                path_counts[neighbor] = 0
            path_counts[neighbor] += path_counts[current]

    return path_counts[dst] if dst in path_counts else 0
