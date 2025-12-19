import sys
from graph import count_paths


if __name__ == "__main__":
    neighbors: dict[str, set[str]] = {"out": set()}
    for line in sys.stdin.readlines():
        line = line.replace(":", "").split()
        neighbors[line[0]] = set(line[1:])

    print(f"device count: {len(neighbors)}")
    print(count_paths("you", "out", neighbors))
