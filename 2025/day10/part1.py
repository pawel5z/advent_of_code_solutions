import sys
from functools import reduce
from tqdm import tqdm


def neighbours(node: int, transitions: list[int]) -> list[int]:
    return [node ^ transition for transition in transitions]


def find_shortest_path_length(bit_count: int, dest: int, transitions: list[int]) -> int:
    queue: list[int] = [0]
    to_visit: list[bool] = [False] * (2 ** bit_count)
    to_visit[0] = True
    distance: list[int] = [-1] * (2**bit_count)
    distance[0] = 0
    while queue:
        current = queue.pop(0)
        for neighbour in neighbours(current, transitions):
            if to_visit[neighbour]:
                continue
            to_visit[neighbour] = True
            distance[neighbour] = distance[current] + 1
            queue.append(neighbour)
    return distance[dest]



if __name__ == "__main__":
    total_presses = 0
    for line in tqdm(sys.stdin.readlines()):
        specs = line.strip().split()
        target_state = int("".join(reversed(specs[0][1:-1])).replace(".", "0").replace("#", "1"), 2)
        state_bits_count = len(specs[0]) - 2
        transition_specs = specs[1:-1]
        transitions = []
        for transition_spec in transition_specs:
            transitions.append(reduce(
                lambda acc, e: acc | (1 << e),
                map(int, transition_spec[1:-1].split(",")),
                0
            ))
        # print(f"{target_state:b}")
        # print(list(map(lambda a: f"{a:b}", transitions)))
        press_count = find_shortest_path_length(state_bits_count, target_state, transitions)
        # print(press_count)
        total_presses += press_count
    print(total_presses)
