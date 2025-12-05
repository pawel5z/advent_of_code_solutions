import sys


if __name__ == "__main__":
    ranges = []
    end_of_ranges = False
    fresh_count = 0
    for line in sys.stdin.readlines():
        if line == "\n":
            end_of_ranges = True
        elif end_of_ranges:
            id = int(line.strip())
            if any(map(lambda e: e[0] <= id <= e[1], ranges)):
                fresh_count += 1
        else:
            ranges.append(tuple(map(int, line.strip().split("-"))))
    print(fresh_count)
