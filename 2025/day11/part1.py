import sys


def compute_path_count(neighbors: dict[str, set[str]]) -> int:
    preds: dict[str, set[str]] = {node: set() for node in neighbors}

    queue: list[str] = ["you"]
    marked: set[str] = {"you"}
    while queue:
        current = queue.pop(0)
        for neighbor in neighbors[current]:
            preds[neighbor].add(current)
            if neighbor not in marked:
                marked.add(neighbor)
                queue.append(neighbor)

    count = 0
    stack: list[str] = ["out"]
    while stack:
        current = stack.pop()
        if current == "you":
            count += 1
        for pred in preds[current]:
            stack.append(pred)

    return count


if __name__ == "__main__":
    neighbors: dict[str, set[str]] = {"out": set()}
    for line in sys.stdin.readlines():
        line = line.replace(":", "").split()
        neighbors[line[0]] = set(line[1:])

    print(f"device count: {len(neighbors)}")
    print(compute_path_count(neighbors))
