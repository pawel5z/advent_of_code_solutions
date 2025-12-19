import sys
from graph import count_paths, check_cycle
from itertools import permutations


if __name__ == "__main__":
    neighbors: dict[str, list[str]] = {"out": []}
    for line in sys.stdin.readlines():
        line = line.replace(":", "").split()
        neighbors[line[0]] = line[1:]

    print(f"device count: {len(neighbors)}")
    print(f"cycle present: {check_cycle(neighbors)}")
    print(sum(
        count_paths("svr", proxy1, neighbors)
        * count_paths(proxy1, proxy2, neighbors)
        * count_paths(proxy2, "out", neighbors)
        for proxy1, proxy2 in permutations(["dac", "fft"], 2)
    ))
