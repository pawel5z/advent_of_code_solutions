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
        # Prioritize buttons belonging to counter that are incremented by the smallest number of buttons.
        # Within such set of buttons prioritize the ones incrementing the most counters with single press.
        for counter_idx in sorted(range(len(press_sources)), key=lambda counter_idx: len(press_sources[counter_idx])):
            for button_idx in sorted(press_sources[counter_idx], key=lambda b: len(buttons[b]), reverse=False):
                if press_state[button_idx] == -1:
                    return (counter_idx, button_idx)


    def get_refined_min_press(considered_button_idx: int, press_state: list[int]) -> int:
        min_press = -1
        for counter_idx in range(len(dst)):
            if considered_button_idx not in press_sources[counter_idx]:
                continue
            min_press_candidate = dst[counter_idx]
            for button_idx in press_sources[counter_idx]:
                if press_state[button_idx] == -1:
                    if button_idx != considered_button_idx:
                        min_press_candidate -= max_presses[button_idx]
                else:
                    min_press_candidate -= press_state[button_idx]
            min_press = max(min_press, min_press_candidate)
        return max(0, min_press)


    def get_refined_max_press(considered_button_idx: int, press_state: list[int]) -> int:
        """Difference to target value of specified counter given specified press_state of buttons.
        """
        max_press = math.inf
        for counter_idx in range(len(dst)):
            if considered_button_idx not in press_sources[counter_idx]:
                continue
            max_press_candidate = dst[counter_idx]
            for button_idx in press_sources[counter_idx]:
                if press_state[button_idx] == -1:
                    if button_idx != considered_button_idx:
                        max_press_candidate -= min_presses[button_idx]
                else:
                    max_press_candidate -= press_state[button_idx]
            max_press_candidate = min(max_presses[considered_button_idx], max_press_candidate)
            max_press = min(max_press, max_press_candidate)
        return max_press
        # return min(max_presses[considered_button_idx], max_press_candidate)


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
        counter_idx, button_idx = get_unassigned_button_idx(press_state)
        refined_min_press = get_refined_min_press(button_idx, press_state)
        refined_max_press = get_refined_max_press(button_idx, press_state)
        for candidate_press_count in range(refined_min_press, refined_max_press + 1):
            candidate_press_state = list(press_state)
            candidate_press_state[button_idx] = candidate_press_count
            candidate_counter_state = get_counter_state(candidate_press_state)
            press_count = sum(v for v in candidate_press_state if v >= 0)
            if any(candidate_counter_state[i] > dst[i] for i in range(len(dst))):
                # print(f">>> skipping {min(press_capacity, max_presses[button_idx]) - candidate_press_count + 1} calls")
                return
            if press_count + greatest_difference(candidate_counter_state, dst) >= min_so_far:
                return
            if all(count >= 0 for count in candidate_press_state):
                reached_bottom_count += 1
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
    for solution in get_solutions(initial_press_state):
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
        # break
    print(total_presses)
