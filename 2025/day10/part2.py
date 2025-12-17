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

    # Mapping of button idx to selected number of presses. -1 means not defined yet.
    initial_press_state: dict[int, int] = {i: -1 for i in range(len(buttons))}


    def get_solutions(press_state: dict[int, int]) -> Iterator[dict[int, int]]:
        # TODO
        return


    return min(
        sum(v for v in solution.values()) for solution in get_solutions(initial_press_state)
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
        break
    print(total_presses)
