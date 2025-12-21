import sys
from tqdm import tqdm
from typing import Iterator
import math


def least_press_count(dst: tuple[int], buttons: list[list[int]]) -> int:
    # max number of presses for each button
    max_presses: list[int] = [min(dst[i] for i in button) for button in buttons]

    # min number of presses for each button
    min_presses: list[int] = []
    for i in range(len(buttons)):
        other_buttons = [] # buttons incrementing at least 1 common counter with button i
        for j in range(len(buttons)):
            if i == j:
                continue
            for influenced_counter_idx in buttons[j]:
                if influenced_counter_idx in buttons[i]:
                    other_buttons.append(j)
                    break

        min_presses.append(
            max(
                0,
                max_presses[i] - sum(map(lambda j: max_presses[j], other_buttons))
            )
        )
    # print([(min_presses[i], max_presses[i]) for i in range(len(buttons))])

    # dst idx to list of buttons incrementing it
    press_sources: list[list[int]] = []
    for i in range(len(dst)):
        press_sources.append([])
        for button_idx, button in enumerate(buttons):
            for counter_idx in button:
                if counter_idx == i:
                    press_sources[i].append(button_idx)
    # print(press_sources)

    # Button idx to selected number of presses. -1 means not defined yet.
    initial_press_state: list[int] = [-1] * len(buttons)


    def get_counter_state(press_state: list[int]) -> tuple[int]:
        # assert(all(count >= 0 for count in press_state))
        counters = [0] * len(dst)
        for button_idx, count in enumerate(press_state):
            if count == -1:
                continue
            for counter_idx in buttons[button_idx]:
                counters[counter_idx] += count
        return tuple(counters)


    def get_unassigned_button_idx(press_state: list[int]) -> tuple[int, int]:
        # Fail-fast strategy.
        # Starting with buttons incrementing counters having the lowest target value,
        # find the first button with unassigned value.
        for counter_idx in sorted(range(len(dst)), key=lambda counter_idx: dst[counter_idx]):
            for button_idx in sorted(press_sources[counter_idx], key=lambda b: len(buttons[b]), reverse=True):
                if press_state[button_idx] == -1:
                    return (counter_idx, button_idx)


    def get_refined_min_press(counter_idx: int, considered_button_idx: int, press_state: list[int]) -> int:
        min_press = dst[counter_idx]
        for button_idx in press_sources[counter_idx]:
            if press_state[button_idx] == -1:
                if button_idx != considered_button_idx:
                    min_press -= max_presses[button_idx]
            else:
                min_press -= press_state[button_idx]
        return max(0, min_press)


    def get_refined_max_press(counter_idx: int, considered_button_idx: int, press_state: list[int]) -> int:
        """Difference to target value of specified counter given specified press_state of buttons.
        """
        max_press = dst[counter_idx]
        for button_idx in press_sources[counter_idx]:
            if press_state[button_idx] == -1:
                if button_idx != considered_button_idx:
                    max_press -= min_presses[button_idx]
            else:
                max_press -= press_state[button_idx]
        return min(max_presses[considered_button_idx], max_press)


    reached_bottom_count = 0
    solution_count = 0
    min_so_far = math.inf
    def get_solutions(press_state: list[int]) -> Iterator[list[int]]:
        nonlocal reached_bottom_count
        nonlocal solution_count
        nonlocal min_so_far
        if all(count >= 0 for count in press_state):
            reached_bottom_count += 1
            if get_counter_state(press_state) == dst:
                solution_count += 1
                min_so_far = min(min_so_far, sum(press_state))
                # print(press_state)
                yield press_state
            else:
                # print(press_state, sum(press_state), get_counter_state(press_state))
                pass
            return

        counter_idx, button_idx = get_unassigned_button_idx(press_state)
        refined_min_press = get_refined_min_press(counter_idx, button_idx, press_state)
        refined_max_press = get_refined_max_press(counter_idx, button_idx, press_state)
        for candidate_press_count in range(refined_min_press, refined_max_press + 1):
            candidate_press_state = list(press_state)
            candidate_press_state[button_idx] = candidate_press_count
            candidate_counter_state = get_counter_state(candidate_press_state)
            if sum(v for v in candidate_press_state if v >= 0) >= min_so_far:
                return
            if any(candidate_counter_state[i] > dst[i] for i in range(len(dst))):
                # print(f">>> skipping {min(press_capacity, max_presses[button_idx]) - candidate_press_count + 1} calls")
                return
            yield from get_solutions(candidate_press_state)


    max_counter = max(dst)
    result = math.inf
    for solution in get_solutions(initial_press_state):
        result = min(result, sum(solution))
        if result == max_counter:
            break
    print(f"bottom reached {reached_bottom_count} times")
    print(f"solution reached {solution_count} times")
    return result


if __name__ == "__main__":
    total_presses = 0
    for line in tqdm(sys.stdin.readlines()):
        specs = line.strip().split()
        target_state = tuple(map(int, specs[-1][1:-1].split(",")))
        button_specs = specs[1:-1]
        buttons = []
        for button_spec in button_specs:
            buttons.append(list(map(int, button_spec[1:-1].split(","))))
        press_count = least_press_count(target_state, buttons)
        total_presses += press_count
        # break
    print(total_presses)
