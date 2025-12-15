import sys
from functools import reduce
from tqdm import tqdm
from copy import deepcopy
import heapq
import math


def max_allowed_press_count(state: tuple[int], transition: list[int]) -> int:
    return math.ceil(min(state[i] for i in transition) / 2)


def unpress(state: tuple[int], transition: list[int]) -> tuple[tuple[int], int]:
    press_count = max_allowed_press_count(state, transition)
    if press_count == 0:
        return state, press_count
    ret = list(state)
    for i in transition:
        ret[i] -= press_count
    return tuple(ret), press_count


def predecessors(state: tuple[int], transitions: list[list[int]]) -> list[tuple[tuple[int], int]]:
    return [unpress(state, transition) for transition in transitions]


def least_press_count(dest: tuple[int], transitions: list[list[int]]) -> int:
    known_counts: dict[tuple[int], int] = {}

    def aux(dest: tuple[int]) -> int:
        if dest in known_counts:
            print(dest)
            return known_counts[dest]
        if any(v < 0 for v in dest):
            return math.inf
        if (all(v == 0 for v in dest)):
            return 0
        result = min(
            (aux(pred) + press_count for pred, press_count in predecessors(dest, transitions) if press_count > 0),
            default=math.inf
        )
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
        break
    print(total_presses)
