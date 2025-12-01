from typing import List, Tuple, Set


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


def get_well_order(rules: List[Tuple[int, int]]) -> List[int]:
    """
    Forget it. It is not guaranteed that input rules define directed acyclic graph.

    That is - sort rules topologically using
    https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
    """
    rules_set = set((pred, succ) for (pred, succ) in rules)
    result: List[int] = []

    unpreceded_pages: Set[int] = set()
    for pred, _ in rules_set:
        unpreceded_pages.add(pred)
    for _, succ in rules_set:
        if succ in unpreceded_pages:
            unpreceded_pages.remove(succ)

    while len(unpreceded_pages) > 0:
        page = unpreceded_pages.pop()
        result.append(page)
        rules_set_list_view = list(rules_set)
        for (pred, succ) in rules_set_list_view:
            if pred == page:
                rules_set.remove((pred, succ))
                if not any(map(lambda rule: rule[1] == succ, rules_set)):
                    unpreceded_pages.add(succ)

    return result


def get_corrected_order(rules: List[Tuple[int, int]], pages: List[int]) -> List[int]:
    well_ordered_pages: List[int] = []
    for page in pages:
        for i in range(len(well_ordered_pages) + 1):
            candidate = list(well_ordered_pages)
            candidate.insert(i, page)
            if well_ordered(rules, candidate):
                well_ordered_pages = candidate
                break
    return well_ordered_pages


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
            if not well_ordered(rules, pages):
                well_ordered_pages = get_corrected_order(rules, pages)
                result += well_ordered_pages[len(well_ordered_pages) // 2]
        except EOFError:
            break

    print(result)
