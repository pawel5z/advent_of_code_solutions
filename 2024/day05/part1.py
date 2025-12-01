from typing import List, Tuple


def well_ordered(rules: List[Tuple[int, int]], pages: List[int]) -> bool:
    # Check preceding correctness.
    for i in range(len(pages)):
        for j in range(i):
            pred = pages[j]
            succ = pages[i]
            for rule in rules:
                if rule == (succ, pred):
                    return False

    return True


if __name__ == "__main__":
    rules: List[Tuple[int, int]] = []

    while True:
        rule_text_parts = input().split('|')
        if len(rule_text_parts) < 2:
            break
        rules.append(tuple(map(int, rule_text_parts)))

    result = 0

    while True:
        try:
            pages = list(map(int, input().split(',')))
            if well_ordered(rules, pages):
                result += pages[len(pages) // 2]
        except EOFError:
            break

    print(result)
