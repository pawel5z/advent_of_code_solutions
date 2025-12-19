import sys


def check_cycle(neighbors: dict[str, set[str]]) -> bool:
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


def compute_path_count(src: str, dest: str, neighbors: dict[str, set[str]]) -> int:
    queue: list[str] = [src]
    # metadata contains number of paths going into a node, respectively:
    # without dac and fft
    # with dac only
    # with fft only
    # with both dac and fft
    node_meta: dict[str, tuple[int, int, int, int]] = {src: (1, 0, 0, 0)}
    while queue:
        current = queue.pop(0)
        no, dac, fft, both = node_meta[current]
        # print(f"{current} {node_meta[current]}")

        match current:
            case "dac":
                if fft:
                    both += fft
                    fft = 0
                    # dac = 0
                dac += no
                no = 0
            case "fft":
                if dac:
                    both += dac
                    dac = 0
                    # fft = 0
                fft += no
                no = 0
        node_meta[current] = (no, dac, fft, both)
        # print(f"{current} {node_meta[current]}")

        for neighbor in neighbors[current]:
            if neighbor in node_meta:
                neighbor_meta = node_meta[neighbor]
                node_meta[neighbor] = (
                    neighbor_meta[0] + no,
                    neighbor_meta[1] + dac,
                    neighbor_meta[2] + fft,
                    neighbor_meta[3] + both,
                )
            else:
                queue.append(neighbor)
                node_meta[neighbor] = (no, dac, fft, both)

    # print(f"svr {node_meta["svr"]}")
    # print(f"out {node_meta["out"]}")
    # for k, v in sorted(node_meta.items()):
    #     print(k, v)
    return node_meta[dest][-1]


if __name__ == "__main__":
    neighbors: dict[str, set[str]] = {"out": set()}
    for line in sys.stdin.readlines():
        line = line.replace(":", "").split()
        neighbors[line[0]] = set(line[1:])

    print(f"cycle present: {check_cycle(neighbors)}")
    print(f"device count: {len(neighbors)}")
    print(compute_path_count("svr", "out", neighbors))
