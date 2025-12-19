def check_cycle(neighbors: dict[str, list[str]]) -> bool:
    visited: set[str] = set()
    finished: set[str] = set()

    def dfs(node: str) -> bool:
        if node in finished:
            return False
        if node in visited:
            return True # cycle found
        visited.add(node)
        for neighbor in neighbors[node]:
            if dfs(neighbor):
                return True
        finished.add(node)

    return any(dfs(node) for node in neighbors)


def count_paths(src: str, dst: str, neighbors: dict[str, list[str]]) -> int:
    path_counts: dict[str, int] = {src: 1}
    queue: list[str] = topological_sort(neighbors)
    queue = queue[queue.index(src):]

    while queue:
        current = queue.pop(0)
        if current not in path_counts:
            continue
        for neighbor in neighbors[current]:
            if neighbor not in path_counts:
                path_counts[neighbor] = 0
            path_counts[neighbor] += path_counts[current]

    return path_counts[dst] if dst in path_counts else 0


def topological_sort(neighbors: dict[str, list[str]]) -> list[str]:
    result: list[str] = []
    processed: set[str] = set()
    marked: set[str] = set()

    def dfs(node: str):
        marked.add(node)
        for neighbor in neighbors[node]:
            if neighbor not in marked:
                dfs(neighbor)
        processed.add(node)
        result.append(node)

    for node in neighbors:
        if node not in processed:
            dfs(node)
    result.reverse()
    return result
