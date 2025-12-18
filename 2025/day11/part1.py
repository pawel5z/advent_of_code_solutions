import sys


def compute_path_count(neighbors: dict[str, set[str]]) -> int:
    queue: list[str] = ["you"]
    count = 0
    while queue:
        current = queue.pop(0)
        if current == "out":
            count += 1
        for neighbor in neighbors[current]:
            queue.append(neighbor)

    return count


if __name__ == "__main__":
    neighbors: dict[str, set[str]] = {"out": set()}
    for line in sys.stdin.readlines():
        line = line.replace(":", "").split()
        neighbors[line[0]] = set(line[1:])

    print(f"device count: {len(neighbors)}")
    print(compute_path_count(neighbors))
