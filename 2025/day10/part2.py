import sys
from functools import reduce
from tqdm import tqdm
from copy import deepcopy
import heapq


def h(node: tuple[int], dest: tuple[int]) -> int:
    return sum((dest[i] - node[i] for i in range(len(dest))))


def transit(node: tuple[int], transition: list[int]) -> list[int]:
    ret = list(node)
    for i in transition:
        ret[i] += 1
    return tuple(ret)


def neighbours(node: tuple[int], transitions: list[list[int]]) -> list[tuple[int]]:
    return [transit(node, transition) for transition in transitions]


def find_shortest_path_length(dest: tuple[int], transitions: list[list[int]]) -> int:
    source = (0,) * len(dest)
    queue: list[tuple[int, tuple[int]]] = [(0, source)]
    heapq.heapify(queue)
    marked_visit: set[tuple[int]] = {source}
    distance: dict[tuple[int], int] = {source: 0}
    while queue:
        _, current = heapq.heappop(queue)
        for neighbour in neighbours(current, transitions):
            if neighbour in marked_visit:
                continue
            marked_visit.add(neighbour)
            if any((neighbour[i] > dest[i]) for i in range(len(dest))):
                continue
            distance[neighbour] = distance[current] + 1
            if neighbour == dest:
                break
            heapq.heappush(queue, (distance[neighbour] + h(neighbour, dest), neighbour))
    return distance[dest]


if __name__ == "__main__":
    total_presses = 0
    for line in tqdm(sys.stdin.readlines()):
        specs = line.strip().split()
        target_state = tuple(map(int, specs[-1][1:-1].split(",")))
        transition_specs = specs[1:-1]
        transitions = []
        for transition_spec in transition_specs:
            transitions.append(list(map(int, transition_spec[1:-1].split(","))))
        press_count = find_shortest_path_length(target_state, transitions)
        total_presses += press_count
    print(total_presses)
