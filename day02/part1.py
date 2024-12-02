from typing import Iterable, Callable


def is_monotonic_and_safe[T](less_operator: Callable[[T, T], bool], sequence: Iterable[T]) -> bool:
    previous = None
    for element in sequence:
        if previous is None:
            previous = element
            continue

        delta = abs(previous - element)
        if not less_operator(previous, element) or delta < 1 or delta > 3:
            return False

        previous = element

    return True


if __name__ == "__main__":
    safe_reports_count = 0

    while True:

        try:
            report = list(map(int, input().split()))
        except EOFError:
            break

        if is_monotonic_and_safe(lambda a, b: a < b, report) or is_monotonic_and_safe(lambda a, b: a > b, report):
            safe_reports_count += 1

    print(safe_reports_count)
