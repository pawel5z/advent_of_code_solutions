import sys
from functools import reduce


if __name__ == "__main__":
    ranges = []
    end_of_ranges = False
    for line in sys.stdin.readlines():
        if line == "\n":
            break

        b, e = tuple(map(int, line.strip().split("-")))
        ranges.append((b, e))
        changed = True
        comp_idx = len(ranges) - 1
        while changed:
            changed = False
            b, e = ranges[comp_idx]
            for i in range(len(ranges)):
                if i == comp_idx:
                    continue
                b1, e1 = ranges[i]
                if e < b1 or e1 < b:
                    continue
                ranges[i] = (min(b, b1), max(e, e1))
                changed = True
                ranges.pop(comp_idx)
                comp_idx = i - 1 if comp_idx < i else i
                break

    for r in ranges:
        print(r)
    print(reduce(lambda acc, e: acc + e[1] - e[0] + 1, ranges, 0))
