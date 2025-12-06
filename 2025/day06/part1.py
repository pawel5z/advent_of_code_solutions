import sys
from functools import reduce


if __name__ == "__main__":
    columns = []
    total = 0
    for line in sys.stdin.readlines():
        if "+" in line or "*" in line:
            for i, op in enumerate(line.split()):
                match op:
                    case "+":
                        total += reduce(lambda acc, e: acc + e, columns[i], 0)
                    case "*":
                        total += reduce(lambda acc, e: acc * e, columns[i], 1)
        else:
            for i, n in enumerate(map(int, line.split())):
                if len(columns) == i:
                    columns.append([])
                columns[i].append(n)
    print(total)
