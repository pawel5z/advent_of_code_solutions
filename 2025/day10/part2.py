import sys
from tqdm import tqdm
from typing import Iterator
import math


def least_press_count(dst: tuple[int], buttons: list[list[int]]) -> int:
    # dst idx to list of buttons incrementing it
    press_sources: list[list[int]] = []
    for i in range(len(dst)):
        press_sources.append([])
        for button_idx, button in enumerate(buttons):
            for counter_idx in button:
                if counter_idx == i:
                    press_sources[i].append(button_idx)
    # print(press_sources)


    def get_counter_state(press_state: list[int]) -> tuple[int]:
        # assert(all(count >= 0 for count in press_state))
        counters = [0] * len(dst)
        for button_idx, count in enumerate(press_state):
            if count == -1:
                continue
            for counter_idx in buttons[button_idx]:
                counters[counter_idx] += count
        return tuple(counters)


    def get_max_press_list(press_state: list[int]) -> list[int]:
        result: list[int] = []
        for considered_button_idx in range(len(buttons)):
            max_press = math.inf
            for counter_idx, press_source in enumerate(press_sources):
                if considered_button_idx not in press_source:
                    continue
                max_press_candidate = dst[counter_idx]
                for button_idx in press_source:
                    if press_state[button_idx] != -1:
                        max_press_candidate -= press_state[button_idx]
                max_press = min(max_press, max_press_candidate)
            result.append(max_press)
        return result


    def get_min_press_list(press_state: list[int], max_presses: list[int]) -> list[int]:
        result: list[int] = []
        for considered_button_idx in range(len(buttons)):
            min_press = 0
            for counter_idx, press_source in enumerate(press_sources):
                if considered_button_idx not in press_source:
                    continue
                min_press_candidate = dst[counter_idx]
                for button_idx in press_source:
                    if press_state[button_idx] == -1:
                        if button_idx != considered_button_idx:
                            min_press_candidate -= max_presses[button_idx]
                    else:
                        min_press_candidate -= press_state[button_idx]
                min_press = max(min_press, min_press_candidate)
            result.append(min_press)
        return result


    def greatest_difference(c1: list[int], c2: list[int]) -> int:
        return max(abs(c1[i] - c2[i]) for i in range(len(dst)))


    call_count = 0
    reached_bottom_count = 0
    solution_count = 0
    min_so_far = math.inf
    def get_solutions(press_state: list[int]) -> Iterator[list[int]]:
        nonlocal call_count
        nonlocal reached_bottom_count
        nonlocal solution_count
        nonlocal min_so_far

        call_count += 1
        max_presses = get_max_press_list(press_state)
        min_presses = get_min_press_list(press_state, max_presses)
        # button_idx = sorted(( for i in range(len(buttons)) if press_state[i] == -1))[0]
        button_idx = min(
            (i for i in range(len(buttons)) if press_state[i] == -1),
            # key=lambda i: (min(dst[j] for j in buttons[i]), (max_presses[i] - min_presses[i]), len(buttons[i])), # ok
            # key=lambda i: ((max_presses[i] - min_presses[i]), min(dst[j] for j in buttons[i]), len(buttons[i])), # better
            key=lambda i: ((max_presses[i] - min_presses[i]), len(buttons[i]), min(dst[j] for j in buttons[i])), # best so far
        )
        # print(f"currently {get_counter_state(press_state)}")
        # print(f"incrementing {buttons[button_idx]}; considering presses from {refined_min_press} to {refined_max_press}")
        for candidate_press_count in range(min_presses[button_idx], max_presses[button_idx] + 1):
            candidate_press_state = list(press_state)
            candidate_press_state[button_idx] = candidate_press_count
            candidate_counter_state = get_counter_state(candidate_press_state)
            # print(candidate_counter_state)
            press_count = sum(v for v in candidate_press_state if v >= 0)
            if any(candidate_counter_state[i] > dst[i] for i in range(len(dst))):
                # print(f">>> skipping {min(press_capacity, max_presses[button_idx]) - candidate_press_count + 1} calls")
                return
            if press_count + greatest_difference(candidate_counter_state, dst) >= min_so_far:
                return
            if all(count >= 0 for count in candidate_press_state):
                reached_bottom_count += 1
                # print(candidate_counter_state)
                if candidate_counter_state == dst:
                    solution_count += 1
                    if press_count < min_so_far:
                        min_so_far = min(min_so_far, press_count)
                        yield candidate_press_state
                        # print(f">>> {candidate_press_state, press_count, candidate_counter_state}")
                else:
                    # print(candidate_press_state, press_count, candidate_counter_state)
                    pass
                return
            else:
                yield from get_solutions(candidate_press_state)


    max_counter = max(dst)
    result = math.inf
    for solution in get_solutions([-1] * len(buttons)):
        result = min(result, sum(solution))
        if result == max_counter:
            break
    print(f"number of calls: {call_count}")
    print(f"bottom reached {reached_bottom_count} times")
    print(f"solution reached {solution_count} times")
    return result


if __name__ == "__main__":
    total_presses = 0
    for l, line in enumerate(tqdm(sys.stdin.readlines())):
        specs = line.strip().split()
        target_state = tuple(map(int, specs[-1][1:-1].split(",")))
        button_specs = specs[1:-1]
        buttons = []
        for button_spec in button_specs:
            buttons.append(list(map(int, button_spec[1:-1].split(","))))
        print(f"{l+1})")
        press_count = least_press_count(target_state, buttons)
        total_presses += press_count
        break
    print(total_presses)
