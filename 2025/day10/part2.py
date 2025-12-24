import sys
from tqdm import tqdm
from typing import Iterator
import math
import scipy.optimize


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

    result = scipy.optimize.linprog(
        [1] * len(buttons),
        None,
        None,
        [[int(b in press_sources[counter_idx]) for b in range(len(buttons))] for counter_idx in range(len(dst))],
        dst,
        [(min_presses[b], max_presses[b]) for b in range(len(buttons))],
        integrality=1,
    )

    print(result.message)
    print(list(map(int, result.x)), int(result.fun))
    return int(result.fun)


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
    print(total_presses)
