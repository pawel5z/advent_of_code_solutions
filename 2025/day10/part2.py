import sys
from tqdm import tqdm
from typing import Iterator


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
        assert(all(count >= 0 for count in press_state))
        counters = [0] * len(dst)
        for button_idx, count in enumerate(press_state):
            for counter_idx in buttons[button_idx]:
                counters[counter_idx] += count
        return tuple(counters)


    def get_unassigned_button_idx(press_state: list[int]) -> tuple[int, int]:
        # Fail-fast strategy.
        # Starting with buttons incrementing counters having the lowest target value,
        # find the first button with unassigned value.
        for counter_idx in sorted(range(len(dst)), key=lambda counter_idx: dst[counter_idx]):
            for button_idx in press_sources[counter_idx]:
                if press_state[button_idx] == -1:
                    return (counter_idx, button_idx)


    def get_press_capacity(counter_idx, press_state: list[int]) -> int:
        press_capacity = dst[counter_idx]
        for button_idx in press_sources[counter_idx]:
            if press_state[button_idx] == -1:
                press_capacity -= min_presses[button_idx]
            else:
                press_capacity -= press_state[button_idx]
        return press_capacity


    def get_solutions(press_state: list[int]) -> Iterator[list[int]]:
        if all(count >= 0 for count in press_state):
            if get_counter_state(press_state) == dst:
                yield press_state
            return

        counter_idx, button_idx = get_unassigned_button_idx(press_state)
        target_value = dst[counter_idx]
        # add min press count of considered button that was subtracted by get_press_capacity
        press_capacity = get_press_capacity(counter_idx, press_state) + min_presses[button_idx]
        if press_capacity < min_presses[button_idx]:
            return
        for candidate_press_count in range(min_presses[button_idx], min(press_capacity, max_presses[button_idx]) + 1):
            candidate_press_state = list(press_state)
            candidate_press_state[button_idx] = candidate_press_count
            yield from get_solutions(candidate_press_state)


    return min(
        sum(press_count for press_count in solution) for solution in get_solutions(initial_press_state)
    )


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
