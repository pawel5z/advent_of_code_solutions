import sys
from functools import reduce
from tqdm import tqdm
from copy import deepcopy
import heapq
import math


def unpress(state: tuple[int], transition: list[int]) -> list[int]:
    ret = list(state)
    for i in transition:
        ret[i] -= 1
    return tuple(ret)


def predecessors(state: tuple[int], transitions: list[list[int]]) -> list[tuple[int]]:
    return [unpress(state, transition) for transition in transitions]


def least_press_count(dest: tuple[int], transitions: list[list[int]]) -> int:
    known_counts: dict[tuple[int], int] = {}

    def aux(dest: tuple[int]) -> int:
        if dest in known_counts:
            return known_counts[dest]
        if any(v < 0 for v in dest):
            return math.inf
        if (all(v == 0 for v in dest)):
            return 0
        result = min((aux(pred) for pred in predecessors(dest, transitions))) + 1
        known_counts[dest] = result
        return result

    return aux(dest)


if __name__ == "__main__":
    total_presses = 0
    for line in tqdm(sys.stdin.readlines()):
        specs = line.strip().split()
        target_state = tuple(map(int, specs[-1][1:-1].split(",")))
        transition_specs = specs[1:-1]
        transitions = []
        for transition_spec in transition_specs:
            transitions.append(list(map(int, transition_spec[1:-1].split(","))))
        press_count = least_press_count(target_state, transitions)
        total_presses += press_count
    print(total_presses)
