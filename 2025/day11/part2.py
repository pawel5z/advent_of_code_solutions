import sys


def compute_path_count(src: str, dest: str, neighbors: dict[str, set[str]]) -> int:
    preds: dict[str, set[str]] = {node: set() for node in neighbors}

    queue: list[str] = [src]
    marked: set[str] = {src}
    while queue:
        current = queue.pop(0)
        for neighbor in neighbors[current]:
            preds[neighbor].add(current)
            if neighbor not in marked:
                marked.add(neighbor)
                queue.append(neighbor)
    print("computed paths")

    count = 0
    stack: list[tuple[str, bool, bool]] = [(dest, False, False)]
    while stack:
        current, visited_dac, visited_fft = stack.pop()
        if current == src and visited_dac and visited_fft:
            count += 1
            print(count)
        if current == "dac":
            visited_dac = True
        if current == "fft":
            visited_fft = True
        for pred in preds[current]:
            stack.append((pred, visited_dac, visited_fft))

    return count


if __name__ == "__main__":
    neighbors: dict[str, set[str]] = {"out": set()}
    for line in sys.stdin.readlines():
        line = line.replace(":", "").split()
        neighbors[line[0]] = set(line[1:])

    print(f"device count: {len(neighbors)}")
    print(compute_path_count("svr", "out", neighbors))
